# App del corso · prototipo (lezioni 1 e 2)

Pubblicata come artifact: https://claude.ai/artifact/PoYsNRcs6eKTS3DW7WdLv4

- `index.html` · l'app (registrazione, percorso delle lezioni, visore slide, quiz a caselle, storico, rimando dall'errore alla slide).
- `app_build.py` · genera `app/corso.json` (capitoli, quiz con risposte e slide da rivedere) e `app/slides/*.jpg` dai PDF in `corso/export/pdf/`.

Progressi per allievo nel `db` dell'artifact, in `data/users/<id>/profile` (privato per ogni allievo); senza `db` restano sul dispositivo.
Progetto completo: documento «Progetto: corso di patente nautica in app e in libro».

## Versione per l'aula (`aula/`)

Pacchetto per il PC dell'istruttore: gli allievi sul wifi della scuola aprono l'app e i progressi restano sul PC.

- `aula/server.py`: server con la sola libreria standard di Python. Registra gli allievi (nome + codice personale di 4-6 cifre), salva i progressi in `dati/allievi.json`, con un backup al giorno, e serve l'area istruttore `/docente`, protetta da PIN.
- `aula/docente.html`: area istruttore, con QR da proiettare, andamento di ogni allievo, quiz più sbagliati, nuovo codice, eliminazione ed export CSV.
- `aula/prepara_pacchetto.py`: rigenera `aula/www/` da `index.html` (caratteri in locale) e lo zip in `corso/export/app/`. Con `--python` include Python portatile per Windows, così non serve installarlo.
- L'app riconosce da sola dove gira: server dell'aula (`api/info`), artifact (archivio `db`) oppure solo il dispositivo.
