# Versioni dell'app

Numerazione `MAGGIORE.MINORE.CORREZIONE`:
- **0.x** mentre l'app è in prova con gli allievi; **1.0.0** al lancio con tutte le lezioni;
- la seconda cifra sale con le novità, la terza con le sole correzioni.

Il numero è in `corso/app/index.html` (`VERSIONE`, `RILASCIO`) e in `corso/app/aula/server.py` (`VERSIONE`): si cambiano insieme.
Si vede in fondo all'app, nell'aiuto, nell'area istruttore e nella finestra del server.

## 0.8.1 · 7 ottobre 2026
- Account di prova più ristretti: nell'app solo le prime 3 slide delle lezioni 1 e 2 con una verifica di esempio (niente schede, numeri d'oro né appendici); nell'area istruttore di prova solo la presentazione «Rotta verso la patente».
- App online: le appendici delle lezioni chiuse restano bloccate anche chiedendole senza «.html».

## 0.8.0 · 7 ottobre 2026
- App online: account di prova per altre scuole, creati dall'istruttore nella nuova scheda «Prove» dell'area istruttore, con scadenza (5 giorni di base). Chi prova vede l'app con le lezioni 1 e 2 (schede, numeri d'oro, appendice E) e un'area istruttore con allievi inventati e cinque presentazioni; mai gli allievi veri né le altre lezioni. Alla scadenza non si apre più niente.

## 0.7.1 · 7 ottobre 2026
- App online: chi entra con l'email dell'istruttore trova in home il pulsante «Area istruttore».

## 0.7.0 · 7 ottobre 2026
- App online per tutto il corso, a casa e in aula, allo stesso indirizzo: l'allievo entra con l'email (Cloudflare Access) e la prima volta scrive solo il nome, senza codice personale; i progressi si salvano online a ogni risposta e, senza rete, si inviano al ritorno della connessione. Le slide delle lezioni aperte si scaricano subito per averle anche offline.
- Area istruttore online (`/docente`, solo con l'email dell'istruttore): classe, risultati, quiz sbagliati, lezioni da aprire (senza ripubblicare), presentazioni da proiettare da qualunque computer.
- Il server dell'aula resta come riserva.

## 0.6.0 · 7 ottobre 2026
- App da casa con tutto il materiale della web app: le 15 lezioni (aperte la 1 e la 2, le altre oscurate), schede riassuntive, numeri d'oro e appendici, con le stesse regole di apertura; tutto disponibile anche senza rete. Logo della scuola nella pagina di accesso.

## 0.5.2 · 7 ottobre 2026
- Indirizzo dell'app da casa: `https://corsonautico-ondaportante.fafiorucci.workers.dev/` (Worker Cloudflare con file statici al posto del progetto Pages).

## 0.5.1 · 7 ottobre 2026
- Indirizzo dell'app da casa: `https://corsonautico-ondaportante.pages.dev/` (progetto Cloudflare Pages «corsonautico-ondaportante»).

## 0.5.0 · 7 ottobre 2026
- App da casa ad accesso riservato: si pubblica su Cloudflare Pages protetto da Cloudflare Access (entrano solo le email ammesse, con un codice via email; sessione di 30 giorni). A ogni apertura con la rete l'app controlla l'accesso: se l'email è stata tolta, cancella slide e quiz dal telefono e chiede di rientrare. Senza rete funziona fino a 7 giorni dall'ultimo controllo riuscito, poi chiede di collegarsi. I progressi restano sul telefono.

## 0.4.0 · 6 ottobre 2026
- Prova dello studio a casa: app «da casa» installabile e offline (`casa/prepara_casa.py`, sito https separato), con «Porta a casa» nell'app dell'aula e «Invia all'aula» nell'app da casa. I progressi viaggiano nel link e si uniscono a quelli del server. Per la prova contiene solo «Rotta verso la patente» e i quiz dei numeri d'oro.

## 0.3.0 · 6 ottobre 2026
- Area istruttore: le presentazioni si aprono nella stessa pagina e «← Elenco» ci riporta senza chiedere il PIN; tra le presentazioni ci sono anche le 15 lezioni; logo e titolo riportano alla classe; versione in basso a destra.
- App in aula: se il server non risponde si continua a lavorare; quiz e slide restano sul telefono e si inviano da soli al ritorno della connessione (unione con i dati del server).

## 0.2.0 · 6 ottobre 2026
- «Rivedi l'argomento»: la slide va a schermo intero (pulsante ⛶; da sola col telefono in orizzontale).
- «N da ripassare» nei capitoli della lezione e nelle lezioni della home porta direttamente ai quiz sbagliati, dal primo.

## 0.1.0 · 6 ottobre 2026
Prima versione numerata.
- Allievi: 15 lezioni (aperte la 1 e la 2), slide a schermo intero, verifiche e raccolte di quiz ufficiali con rimando alla slide e recupero degli errori, schede riassuntive, numeri d'oro, appendici A-M, progressi, profilo (patente, esame, contatti, preferenze, obiettivo settimanale), aiuto per ogni pagina.
- Aula: server per il PC dell'istruttore, area istruttore (classe, QR, presentazioni, lezioni da aprire, aiuto).
- Demo per altre scuole: lezione 1 di esempio, schede, appendici C ed E, area istruttore con dati inventati.
