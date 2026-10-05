# App del corso · prototipo (lezioni 1 e 2)

Pubblicata come artifact: https://claude.ai/artifact/PoYsNRcs6eKTS3DW7WdLv4

- `index.html` · l'app (registrazione, percorso delle lezioni, visore slide, quiz a caselle, storico, rimando dall'errore alla slide).
- `app_build.py` · genera `app/corso.json` (capitoli, quiz con risposte e slide da rivedere) e `app/slides/*.jpg` dai PDF in `corso/export/pdf/`.

Progressi per allievo nel `db` dell'artifact, in `data/users/<id>/profile` (privato per ogni allievo); senza `db` restano sul dispositivo.
Progetto completo: documento «Progetto: corso di patente nautica in app e in libro».
