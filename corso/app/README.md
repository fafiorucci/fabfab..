# App del corso · prototipo (lezioni 1 e 2)

Pubblicata come artifact: https://claude.ai/artifact/PoYsNRcs6eKTS3DW7WdLv4

- `index.html` · l'app (registrazione, percorso delle lezioni, visore slide, quiz a caselle, storico, rimando dall'errore alla slide).
- `app_build.py` · genera `app/corso.json` (capitoli, quiz con risposte e slide da rivedere) e `app/slides/*.jpg` dai PDF in `corso/export/pdf/`.

Progressi per allievo nel `db` dell'artifact, in `data/users/<id>/profile` (privato per ogni allievo); senza `db` restano sul dispositivo.
Progetto completo: documento «Progetto: corso di patente nautica in app e in libro».

## Uso in aula sul wifi della scuola

1. Copiare sul PC del docente la cartella con `index.html`, `corso.json` e `slides/` (generati da `app_build.py`).
2. Avviarla dal PC: `python3 -m http.server 8000` dentro la cartella (su Windows `py -m http.server 8000`) e consentire l'accesso nel firewall per la rete privata.
3. Gli allievi, sullo stesso wifi, aprono `http://<IP del PC>:8000` (l'IP si legge con `ipconfig` / `ip a`).

In questa modalità non c'è l'archivio dell'artifact: i progressi restano nel browser di ogni allievo.
Serve l'isolamento client disattivato sul wifi (spesso attivo sulle reti «ospiti»). Senza internet i caratteri ripiegano su quelli di sistema.
