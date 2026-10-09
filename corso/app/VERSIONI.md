# Versioni dell'app

Numerazione `MAGGIORE.MINORE.CORREZIONE`:
- **0.x** mentre l'app è in prova con gli allievi; **1.0.0** al lancio con tutte le lezioni;
- la seconda cifra sale con le novità, la terza con le sole correzioni.

Il numero è in `corso/app/index.html` (`VERSIONE`, `RILASCIO`) e in `corso/app/aula/server.py` (`VERSIONE`): si cambiano insieme.
Si vede in fondo all'app, nell'aiuto, nell'area istruttore e nella finestra del server.

## 0.14.1 · 9 ottobre 2026
- Scheda «Accessi» anche nella demo e nell'area istruttore del sito delle prove, con un registro di esempio (tre segnalazioni, IP, dispositivi, blocchi e sblocchi da provare).

## 0.14.0 · 9 ottobre 2026
- App online: registro degli accessi per 90 giorni. Per allievo e giorno: aperture dell'app, slide, schede, appendici e quiz; indirizzi IP con la località stimata da Cloudflare; dispositivi (codice casuale dell'app nel cookie `corso_disp`, con tipo di telefono o computer e browser). Il MAC non arriva al server.
- Segnalazioni dei casi sospetti: più di 3 dispositivi in 7 giorni, accesso dall'estero, due luoghi a più di 300 km nella stessa ora. Nuova scheda «Accessi» nell'area istruttore, con il numero delle segnalazioni aperte e il pallino rosso nella «Classe»; il link `…/docente?segnalazione=<id>` apre la segnalazione.
- Blocchi: tutto l'allievo, un suo IP o un suo dispositivo (solo per lui); l'app mostra «Accesso sospeso» e toglie slide e quiz dal telefono, i progressi restano. Sblocco dal dettaglio dell'allievo.
- Email di avviso con il link diretto, se c'è un dominio attivato in Cloudflare Email Service (`EMAIL_DA` in `casa/prepara_casa.py`).
- Consenso dell'app e PDF per gli allievi con la riga sulla registrazione degli accessi.

## 0.13.3 · 9 ottobre 2026
- Caratteri senza internet (app in aula, app online, demo da chiavetta): Nunito Sans e Fredoka con tutti i pesi. Prima Nunito Sans c'era solo in extra-grassetto e tutto il testo usciva in grassetto. Si riscaricano con `aula/scarica_caratteri.py`.

## 0.13.2 · 8 ottobre 2026
- La prima volta, dopo l'entrata, un fumetto sotto il logo avvisa che toccandolo si apre il menu; poi quello sotto «?» per l'aiuto. Ognuno compare una sola volta per dispositivo (non compare più se si è già aperto il menu o l'aiuto) e si chiude da solo dopo 9 secondi.

## 0.13.1 · 8 ottobre 2026
- Il menu a cassetto si apre toccando il logo: tolta l'icona ☰ accanto.

## 0.13.0 · 8 ottobre 2026
- Menu a cassetto: toccando il logo in alto a sinistra (con l'icona ☰) si apre da sinistra il menu, in tutte le pagine: Home, ripasso degli errori, le lezioni (ognuna con panoramica, capitoli, verifiche con l'esito, raccolta quiz, scheda riassuntiva e appendici), le schede riassuntive, le appendici, i progressi, il profilo e l'aiuto. La lezione o il materiale della pagina aperta è già espanso e segnato; le voci chiuse hanno il lucchetto. Si chiude con la ✕, toccando fuori, con Esc o scorrendo verso sinistra.
- Scorrimento col dito come nelle app, solo sul tocco: la slide (lezioni, schede, appendici) e la domanda del quiz seguono il dito ed escono di lato; verso sinistra si va avanti (nel quiz come «Salta →»), verso destra indietro; all'inizio e in fondo la pagina resiste. Sul PC restano pulsanti, frecce e clic sui lati.
- Aiuto aggiornato (menu, quiz uno per pagina).

## 0.12.0 · 8 ottobre 2026
- Appendici nel visore dell'app, come lezioni e schede: stesso sfondo, intestazione e fondo pagina, contatore, «← Indietro / Avanti →», schermo intero e dito per sfogliare; le pagine sono immagini con la filigrana (`AX-NNN.jpg`, da `app_build.py`) e si scaricano per l'uso senza rete. Dalla lezione si torna alla lezione, da Materiali a Materiali.
- App online: subito dopo il primo accesso l'app si apre anche senza rete (prima serviva almeno una risposta salvata).
- I quiz dei numeri d'oro rimandano alla slide della lezione che li spiega (se la lezione è aperta).

## 0.11.1 · 8 ottobre 2026
- Quiz sul telefono: testata su una riga (← Indietro e titolo), domanda e risposte più compatte e senza sillabazione, pulsanti in fondo sempre visibili; la domanda con le risposte sta nello schermo anche sui telefoni piccoli.

## 0.11.0 · 8 ottobre 2026
- Quiz uno per pagina: scelta la risposta si vede subito se è giusta e dopo un attimo si passa da soli alla domanda dopo (dopo un errore un po' di più, per leggere la risposta giusta); «Salta →» e «← Precedente»; in fondo il riepilogo con il punteggio, le domande saltate e gli errori con «Rivedi l'argomento». Ogni risposta si salva subito.
- Home: riepilogo dei progressi su una riga; sui telefoni lo stemma non copre più il saluto.

## 0.10.0 · 8 ottobre 2026
- Home: riepilogo dei progressi nel riquadro con lo stemma (slide studiate, quiz risposti, risposte giuste, quiz da ripassare con il pulsante per farli, giorni all'esame); testi giustificati con la sillabazione.
- Telefoni piccoli: nella pagina di entrata lo stemma è piccolo in alto a destra e il modulo si vede senza scorrere.
- Profilo: dopo «Salva il profilo» c'è «Torna alla home →».
- Il link per tornare indietro («← …») si ripete anche in fondo alle pagine lunghe.
- App online: le appendici si aprono anche dalla copia sul telefono (prima davano errore).

## 0.9.1 · 8 ottobre 2026
- Sito delle prove: il Worker si chiama `corso-nautico-prova` (come su Cloudflare); i link di prova sono `https://corso-nautico-prova.fafiorucci.workers.dev/?p=…`.

## 0.9.0 · 7 ottobre 2026
- Account di prova con link, senza email né codice: nella scheda «Prove» si lascia vuota l'email e si ottiene un link personale (`https://corsonautico-prova.fafiorucci.workers.dev/?p=…`) da mandare alla scuola. Il sito delle prove è un secondo Worker senza Cloudflare Access che contiene solo le 6 slide di prova e «Rotta verso la patente»; alla scadenza o con «Togli» il link smette di funzionare e l'app mostra «Prova terminata».

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
