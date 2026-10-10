# Server meteo per Skipper WebApp

Un server [Open-Meteo](https://github.com/open-meteo/open-meteo) sul tuo PC: l'app chiede i dati meteo prima a lui e, se non risponde, a Open-Meteo pubblico. Così il limite delle 10.000 chiamate al giorno non conta più.

## Cosa serve

- PC acceso quando usi l'app (anche un vecchio PC o un mini PC), con Windows 10/11, macOS o Linux.
- Memoria: 8 GB, meglio 16 GB. Disco: almeno 50 GB liberi, meglio SSD.
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows e Mac) oppure Docker su Linux.

## Installazione

1. Installa Docker Desktop e avvialo.
2. Copia questa cartella `server-meteo` sul PC.
3. Apri il terminale nella cartella (Windows: tasto destro → «Apri nel terminale») e scrivi:

   ```
   docker compose up -d
   ```

   Il server parte e si riavvia da solo all'accensione del PC (se Docker Desktop è impostato per avviarsi con il sistema).
4. Prova: apri nel browser `http://localhost:8080/v1/forecast?latitude=41.77&longitude=12.22&hourly=wind_speed_10m` — deve comparire un testo con i dati.
5. Nell'app: **menu → Impostazioni → Server dei dati meteo**, scrivi `http://localhost:8080` (sullo stesso PC) oppure `http://<indirizzo-del-PC>:8080` (dagli altri dispositivi di casa, es. `http://192.168.1.20:8080`), premi **Prova e confronta** e poi **Salva**.

## Riscaldamento automatico

Il servizio `riscaldamento` ogni ora chiede al server le zone usate dall'app, così i dati sono già pronti quando li apri. Nel file `docker-compose.yml`:

- `ZONA` — zona ampia (ovest sud est nord), di base il Mediterraneo centrale, a passo `PASSO` (0,25°);
- `ZONA_FINE` — la tua zona abituale a passo fine (0,1°), di base da Argentario a Ponza.

Cambiale secondo le tue uscite e riavvia con `docker compose up -d`. Lo stato si vede con `docker compose logs -f riscaldamento`.

**Tempi misurati nelle prove** (ambiente di test con una connessione lenta verso l'archivio):

| | prima richiesta di una zona nuova | richieste successive |
|---|---|---|
| Modelli globali (ECMWF, GFS, UKMO) | 15–35 s | 0,05–0,1 s |
| Modelli ad alta risoluzione (ICON, ARPEGE/AROME, ICON-2I) | 15–75 s | 0,07–0,15 s |
| Onda | 5–55 s | 0,1 s |
| Open-Meteo pubblico, per confronto | ~1 s | ~1 s |

Da casa con la fibra le prime richieste dovrebbero essere molto più veloci (stima: 5 volte), ma non è stato possibile misurarlo. Nel frattempo l'app non aspetta: dopo il tempo massimo impostato (30 s) usa Open-Meteo pubblico e la volta dopo trova i dati pronti sul tuo server.

## Uso da fuori casa (telefono, barca)

Un indirizzo come `192.168.…` funziona solo sulla rete di casa. Per raggiungere il server da ovunque, senza aprire porte sul router:

1. Crea un account gratuito su [Cloudflare](https://dash.cloudflare.com) → **Zero Trust → Networks → Tunnels → Create a tunnel** (tipo *Cloudflared*).
2. Copia il **token** del tunnel, crea il file `.env` (copiando `.env.esempio`) e incollalo dopo `TUNNEL_TOKEN=`.
3. Nel tunnel aggiungi un *Public hostname* (es. `meteo.tuodominio.it`) con servizio `http://open-meteo:8080`.
4. Avvia anche il tunnel: `docker compose --profile tunnel up -d`.
5. Nell'app usa `https://meteo.tuodominio.it`.

Il server contiene solo dati meteo pubblici, quindi può restare aperto: se lo proteggi con Cloudflare Access l’app non riesce più a interrogarlo dal browser.

## Spazio e traffico

- Il server tiene in memoria su disco al massimo `CACHE_SIZE` (20 GB): quando è piena butta via i dati più vecchi.
- Il riscaldamento scarica solo le parti dei file che servono: nelle prove, tutte insieme, alcune centinaia di MB. Ogni nuova corsa dei modelli (ogni 3–6 ore) richiede di riscaricare le parti aggiornate.

## Comandi utili

```
docker compose ps                 # stato
docker compose logs -f            # cosa sta facendo
docker compose pull && docker compose up -d   # aggiornare
docker compose down               # fermare
```

Dati: Open-Meteo (CC BY 4.0), software AGPL-3.0.
