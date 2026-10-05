#!/usr/bin/env python3
"""Corso patente nautica · server per l'aula.

Serve l'app agli allievi collegati allo stesso wifi e tiene i loro progressi
sul computer dell'istruttore, nella cartella «dati».
Solo libreria standard di Python 3.8 o successivo: nessuna installazione.

  Allievi:     http://<indirizzo del PC>:8000
  Istruttore:  http://localhost:8000/docente   (con il PIN mostrato all'avvio)
"""
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import socket
import sys
import threading
import time
import unicodedata
import webbrowser
from datetime import datetime
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

QUI = os.path.dirname(os.path.abspath(__file__))
WWW = os.path.join(QUI, 'www')
DATI = os.path.join(QUI, 'dati')
ARCHIVIO = os.path.join(DATI, 'allievi.json')
CONFIG = os.path.join(DATI, 'config.json')
BACKUP = os.path.join(DATI, 'backup')
PORTE = range(8000, 8011)
MAX_CORPO = 1_000_000

lock = threading.Lock()
tentativi = {}  # chiave nome -> [errori, istante del blocco]


def adesso():
    return datetime.now().isoformat(timespec='seconds')


def scrivi_json(percorso, dati):
    tmp = percorso + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(dati, f, ensure_ascii=False, indent=1)
    os.replace(tmp, percorso)


def leggi_json(percorso, vuoto):
    try:
        with open(percorso, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return vuoto
    except json.JSONDecodeError:
        guasto = percorso + '.guasto-' + datetime.now().strftime('%Y%m%d-%H%M%S')
        shutil.copy(percorso, guasto)
        print(f'ATTENZIONE: {percorso} illeggibile, copiato in {guasto}. Riparto dall\'ultimo backup se c\'è.')
        return vuoto


os.makedirs(BACKUP, exist_ok=True)
config = leggi_json(CONFIG, {})
if not config.get('pin') or 'indirizzo' not in config:
    if not config.get('pin'):
        config['pin'] = f'{secrets.randbelow(10**6):06d}'
    config.setdefault('scuola', 'Corso patente nautica')
    config.setdefault('indirizzo', '')
    scrivi_json(CONFIG, config)
archivio = leggi_json(ARCHIVIO, {'allievi': {}})
if not archivio.get('allievi') and os.listdir(BACKUP):
    ultimo = sorted(os.listdir(BACKUP))[-1]
    archivio = leggi_json(os.path.join(BACKUP, ultimo), {'allievi': {}})


def salva():
    scrivi_json(ARCHIVIO, archivio)
    giorno = os.path.join(BACKUP, 'allievi-' + datetime.now().strftime('%Y%m%d') + '.json')
    if not os.path.exists(giorno):
        shutil.copy(ARCHIVIO, giorno)
        vecchi = sorted(os.listdir(BACKUP))[:-30]
        for v in vecchi:
            os.remove(os.path.join(BACKUP, v))


def chiave(nome):
    n = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore').decode().casefold()
    return ' '.join(re.findall(r'[a-z0-9]+', n))


def impronta(codice, sale):
    return hashlib.pbkdf2_hmac('sha256', codice.encode(), bytes.fromhex(sale), 50_000).hex()


def per_token(token):
    if not token:
        return None, None
    for aid, a in archivio['allievi'].items():
        if hmac.compare_digest(a['token'], token):
            return aid, a
    return None, None


def stato_pulito(corpo):
    stato = {'visti': {}, 'risposte': {}}
    visti = corpo.get('visti') or {}
    risposte = corpo.get('risposte') or {}
    if not isinstance(visti, dict) or not isinstance(risposte, dict):
        raise ValueError('formato non valido')
    for lez, pagine in visti.items():
        if isinstance(lez, str) and len(lez) <= 8 and isinstance(pagine, list):
            stato['visti'][lez] = sorted({int(p) for p in pagine if isinstance(p, int) and 0 < p < 1000})
    for qid, r in risposte.items():
        if isinstance(qid, str) and len(qid) <= 20 and isinstance(r, dict):
            stato['risposte'][qid] = {
                'ok': bool(r.get('ok')),
                'scelta': r.get('scelta') if isinstance(r.get('scelta'), int) else None,
                'ts': str(r.get('ts', ''))[:32],
                'tentativi': max(1, min(int(r.get('tentativi') or 1), 999)),
                'rivisto': bool(r.get('rivisto')),
            }
    return stato


class Gestore(SimpleHTTPRequestHandler):
    server_version = 'CorsoNautico/1'

    def __init__(self, *a, **k):
        super().__init__(*a, directory=WWW, **k)

    def log_message(self, fmt, *args):
        if '/api/' in (self.path or '') and self.command == 'POST' and 'progresso' in self.path:
            return  # niente rumore per ogni risposta salvata
        sys.stderr.write('%s  %s\n' % (datetime.now().strftime('%H:%M:%S'), fmt % args))

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        if self.path.endswith(('.html', '/', '.json')) or '/api/' in self.path:
            self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def guess_type(self, path):
        t = super().guess_type(path)
        if t in ('text/html', 'application/json', 'text/css', 'application/javascript', 'text/javascript', 'text/plain'):
            t += '; charset=utf-8'
        return t

    # ---------- risposte ----------
    def rispondi(self, codice, dati):
        corpo = json.dumps(dati, ensure_ascii=False).encode()
        self.send_response(codice)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def errore(self, codice, testo):
        self.rispondi(codice, {'errore': testo})

    def corpo(self):
        n = int(self.headers.get('Content-Length') or 0)
        if n > MAX_CORPO:
            raise ValueError('richiesta troppo grande')
        dati = json.loads(self.rfile.read(n) or b'{}')
        if not isinstance(dati, dict):
            raise ValueError('formato non valido')
        return dati

    def docente_ok(self):
        pin = self.headers.get('X-Pin', '')
        return hmac.compare_digest(pin.encode(), config['pin'].encode())

    # ---------- GET ----------
    def do_GET(self):
        p = urlsplit(self.path).path
        if p in ('/docente', '/docente/'):
            self.path = '/docente.html'
            return super().do_GET()
        if p == '/api/info':
            return self.rispondi(200, {'aula': True, 'scuola': config.get('scuola', '')})
        if p == '/api/progresso':
            with lock:
                _, a = per_token(self.headers.get('X-Token'))
                if not a:
                    return self.errore(401, 'Accesso scaduto: rientra con nome e codice.')
                return self.rispondi(200, {'nome': a['nome'], 'stato': a['stato']})
        if p == '/api/docente/allievi':
            if not self.docente_ok():
                return self.errore(403, 'PIN errato.')
            with lock:
                elenco = [{'id': aid, 'nome': a['nome'], 'creato': a['creato'], 'ultimo': a['ultimo'], 'stato': a['stato']}
                          for aid, a in archivio['allievi'].items()]
            return self.rispondi(200, {'allievi': elenco, 'indirizzi': indirizzi(self.server.server_port)})
        if p.startswith('/api/'):
            return self.errore(404, 'Non trovato.')
        if p.startswith('/dati') or p.endswith('.py'):
            return self.errore(404, 'Non trovato.')
        return super().do_GET()

    # ---------- POST ----------
    def do_POST(self):
        p = urlsplit(self.path).path
        try:
            dati = self.corpo()
        except (ValueError, json.JSONDecodeError):
            return self.errore(400, 'Richiesta non valida.')

        if p == '/api/accedi':
            nome = ' '.join(str(dati.get('nome', '')).split())[:60]
            codice = str(dati.get('codice', '')).strip()
            k = chiave(nome)
            if not k:
                return self.errore(400, 'Scrivi il tuo nome.')
            if not re.fullmatch(r'\d{4,6}', codice):
                return self.errore(400, 'Il codice personale è di 4 cifre (fino a 6).')
            with lock:
                err, blocco = tentativi.get(k, [0, 0])
                if blocco and time.time() - blocco < 300:
                    return self.errore(429, 'Troppi tentativi: riprova tra qualche minuto o chiedi all\'istruttore.')
                trovato = next(((aid, a) for aid, a in archivio['allievi'].items() if a['chiave'] == k), None)
                if trovato:
                    aid, a = trovato
                    if not hmac.compare_digest(impronta(codice, a['sale']), a['codice']):
                        err += 1
                        tentativi[k] = [err, time.time() if err >= 8 else 0]
                        time.sleep(0.6)
                        return self.errore(403, 'Questo nome è già registrato con un altro codice. '
                                                'Se è il tuo e l\'hai dimenticato, chiedi all\'istruttore un codice nuovo.')
                    tentativi.pop(k, None)
                else:
                    aid = secrets.token_hex(6)
                    sale = secrets.token_hex(16)
                    a = {'nome': nome, 'chiave': k, 'sale': sale, 'codice': impronta(codice, sale),
                         'token': secrets.token_urlsafe(24), 'creato': adesso(), 'ultimo': adesso(),
                         'stato': {'visti': {}, 'risposte': {}}}
                    archivio['allievi'][aid] = a
                    salva()
                    print(f'{datetime.now():%H:%M:%S}  nuovo allievo: {nome}')
                return self.rispondi(200, {'token': a['token'], 'nome': a['nome'], 'stato': a['stato']})

        if p == '/api/progresso':
            with lock:
                _, a = per_token(self.headers.get('X-Token'))
                if not a:
                    return self.errore(401, 'Accesso scaduto: rientra con nome e codice.')
                try:
                    a['stato'] = stato_pulito(dati)
                except (ValueError, TypeError):
                    return self.errore(400, 'Richiesta non valida.')
                a['ultimo'] = adesso()
                salva()
            return self.rispondi(200, {'ok': True})

        if p.startswith('/api/docente/'):
            if not self.docente_ok():
                return self.errore(403, 'PIN errato.')
            with lock:
                a = archivio['allievi'].get(str(dati.get('id', '')))
                if not a:
                    return self.errore(404, 'Allievo non trovato.')
                if p == '/api/docente/codice':
                    nuovo = f'{secrets.randbelow(10**4):04d}'
                    a['sale'] = secrets.token_hex(16)
                    a['codice'] = impronta(nuovo, a['sale'])
                    a['token'] = secrets.token_urlsafe(24)
                    tentativi.pop(a['chiave'], None)
                    salva()
                    return self.rispondi(200, {'codice': nuovo})
                if p == '/api/docente/elimina':
                    del archivio['allievi'][str(dati['id'])]
                    salva()
                    return self.rispondi(200, {'ok': True})
            return self.errore(404, 'Non trovato.')

        return self.errore(404, 'Non trovato.')


def ip_della_rete():
    """L'indirizzo della scheda che porta al router (quella del wifi o del cavo in uso).

    Si chiede al sistema quale scheda userebbe per uscire verso internet: nessun dato viene
    spedito. Le schede virtuali (VirtualBox, VPN, Hyper-V, WSL…) non hanno quella strada e
    restano fuori. Se in dati/config.json c'è "indirizzo", vale quello.
    """
    fisso = re.sub(r'^https?://', '', str(config.get('indirizzo') or '').strip()).split(':')[0].strip('/')
    if fisso:
        return fisso
    for destinazione in ('8.8.8.8', '1.1.1.1', '192.168.255.255'):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect((destinazione, 80))
                ip = s.getsockname()[0]
            if ip and not ip.startswith(('127.', '0.', '169.254.')):
                return ip
        except OSError:
            continue
    return None


def indirizzi(porta):
    ip = ip_della_rete()
    return [f'http://{ip}:{porta}'] if ip else []


def main():
    if not os.path.exists(os.path.join(WWW, 'index.html')):
        sys.exit('Manca la cartella «www» con l\'app: scompatta di nuovo il pacchetto completo.')
    server = None
    for porta in PORTE:
        try:
            server = ThreadingHTTPServer(('0.0.0.0', porta), Gestore)
            break
        except OSError:
            continue
    if not server:
        sys.exit('Nessuna porta libera tra 8000 e 8010.')
    porta = server.server_port
    righe = indirizzi(porta)
    print()
    print('  CORSO PATENTE NAUTICA · server dell\'aula')
    print('  ' + '-' * 46)
    print('  Allievi (stesso wifi), aprite:')
    for r in righe or [f'http://<indirizzo di questo PC>:{porta}']:
        print('     ' + r)
    print('  (Se i telefoni non si collegano, scrivi l\'indirizzo giusto in dati/config.json,')
    print('   alla voce "indirizzo", per esempio "192.168.1.29", e riavvia.)')
    print()
    print(f'  Istruttore:  http://localhost:{porta}/docente')
    print(f'  PIN istruttore:  {config["pin"]}   (si cambia in dati/config.json)')
    print(f'  Allievi registrati: {len(archivio["allievi"])}')
    print()
    print('  Lascia aperta questa finestra durante la lezione. Per chiudere: Ctrl+C.')
    print()
    if '--senza-browser' not in sys.argv:
        threading.Timer(1.0, lambda: webbrowser.open(f'http://localhost:{porta}/docente')).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        with lock:
            salva()
        print('\n  Server chiuso. Progressi salvati in', ARCHIVIO)


if __name__ == '__main__':
    main()
