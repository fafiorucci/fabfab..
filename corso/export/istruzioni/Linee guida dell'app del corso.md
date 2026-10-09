# Linee guida dell'app del corso

9 ottobre 2026 · Fabrizio Fiorucci

Dove si entra, come si iscrivono e si tolgono gli allievi, come far provare l'app ad altre scuole e quali sono i limiti di Cloudflare. App alla versione 0.13.2.

## Indirizzi

Gli allievi usano l'app online; l'istruttore la segue da /docente. Le altre scuole provano dal sito delle prove o dalla demo.

| Cosa | Indirizzo o file | Chi entra |
| --- | --- | --- |
| App del corso (online) | [corsonautico-ondaportante.fafiorucci.workers.dev](https://corsonautico-ondaportante.fafiorucci.workers.dev/) | Allievi con l'email nella policy «Allievi», con il codice che arriva per email |
| Area istruttore (online) | [corsonautico-ondaportante.fafiorucci.workers.dev/docente](https://corsonautico-ondaportante.fafiorucci.workers.dev/docente) | Solo fafiorucci@gmail.com |
| Sito delle prove per altre scuole | corso-nautico-prova.fafiorucci.workers.dev/?p=codice | Chi ha il link personale creato nella scheda «Prove» |
| App in aula senza internet | corso/export/app/Corso patente nautica - app aula.zip | Allievi sul wifi della scuola; istruttore con il PIN |
| Demo online | Pagina «Corso Nautico Demo» | Privata: va condivisa dal menu Condividi della pagina |
| Demo da chiavetta | corso/export/app/Corso patente nautica - demo.zip | Chiunque abbia lo zip |
| Istruzioni per gli allievi | corso/export/istruzioni/Come entrare nell'app del corso.pdf | Da mandare a ogni nuovo allievo |

Attenzione all'indirizzo dell'area istruttore: è /docente per intero (/docent dà «pagina non trovata»).

## Iscrivere un allievo

Un allievo entra solo se la sua email è nella policy «Allievi»; l'app non ha password.

1. Nel pannello Cloudflare apri Zero Trust → Access → Applications, l'applicazione del corso, la policy «Allievi».
2. In Include → Emails aggiungi l'email dell'allievo e salva.
3. Mandagli il PDF «Come entrare nell'app del corso» con il link dell'app.
4. Al primo accesso l'allievo scrive l'email, riceve un codice, scrive il nome nell'app. La sessione dura 30 giorni, poi chiede di nuovo il codice.

Ogni allievo che entra occupa uno dei 50 posti gratuiti di Zero Trust, istruttore compreso.

## Durante il corso

Le lezioni si aprono dall'area istruttore, senza ripubblicare l'app.

- **Aprire una lezione:** area istruttore → scheda «Lezioni» → «Apri agli allievi». Gli allievi la vedono entro mezzo minuto, con scheda e appendici collegate.
- **Seguire la classe:** scheda «Classe», con slide studiate, quiz e risposte giuste di ognuno, i quiz più sbagliati e il riepilogo in CSV.
- **Senza rete:** l'app scarica le slide delle lezioni aperte e funziona offline fino a 7 giorni dall'ultimo controllo dell'accesso. Quiz e progressi si inviano appena torna la rete.
- **Nuova versione dell'app:** gli allievi chiudono e riaprono l'app due volte. La versione si legge in fondo all'app e nell'Aiuto.

## Togliere un allievo e liberare i posti

Il posto si libera con «Remove users»; «Revoke» chiude solo la sessione e il posto resta occupato.

Per un allievo che lascia il corso:

1. Togli la sua email dalla policy «Allievi»: non riceve più il codice.
2. Zero Trust → Team & Resources → Users: selezionalo e fai Action → Revoke, per chiudere la sessione sul telefono.
3. Nella stessa pagina fai Action → Remove users: diventa Inactive e libera il posto.
4. Se vuoi, «Elimina allievo» nell'area istruttore cancella anche i suoi progressi.

A fine corso basta il passo 3 su tutti gli allievi con il posto Active. Chi rientra riprende un posto da solo.

In automatico: Zero Trust → Settings → Admin controls → «Remove inactive users from seats» → Edit, con un periodo da 1 mese a 1 anno. Ogni giorno Cloudflare libera i posti di chi non entra da quel periodo; per corsi di qualche mese vanno bene 1 o 2 mesi.

## Far provare l'app a un'altra scuola

Si crea un link personale di prova dall'area istruttore: non serve l'email e non occupa posti di Zero Trust.

1. Area istruttore → scheda «Prove»: lascia vuota l'email, scrivi il nome della scuola e la scadenza («5 giorni da oggi»).
2. «Copia il link» e mandalo alla scuola.
3. Per chiudere prima: «Togli». Alla scadenza l'app mostra «Prova terminata» e si svuota.

Cosa vede la scuola: lezioni 1 e 2 con le prime 3 slide e la prima verifica, la presentazione «Rotta verso la patente», un'area istruttore con allievi inventati. Niente schede né appendici, e le prove non compaiono nella classe vera.

Una prova con l'email invece del link funziona come un allievo: l'email va aggiunta alla policy «Allievi» e occupa un posto.

## La demo

La demo mostra l'app con contenuti di esempio: lezione 1 fino al capitolo 1, la sua scheda, i numeri d'oro, le appendici C ed E e un'area istruttore con allievi inventati.

- **Online:** la pagina «Corso Nautico Demo». È privata: per farla vedere va condivisa dal menu Condividi della pagina.
- **Da chiavetta o senza internet:** scompatta «Corso patente nautica - demo.zip» e fai doppio clic su index.html (Chrome, Edge, Firefox o Safari). La cartella va tenuta intera; dentro c'è un LEGGIMI.txt.
- I progressi della demo restano solo nel browser di chi la prova.

## Corso in aula senza internet

Con il pacchetto per l'aula il PC dell'istruttore fa da sito del corso: gli allievi si collegano al wifi della scuola e i progressi restano sul PC.

1. Scompatta «Corso patente nautica - app aula.zip» (circa 85 MB, Python incluso).
2. Doppio clic su «Avvia (Windows).bat» (su Mac «Avvia (Mac).command»). Se Windows avvisa, «Ulteriori informazioni» → «Esegui comunque»; al firewall consenti le reti private.
3. Si apre l'area istruttore: entra con il PIN di 6 cifre mostrato nella finestra nera.
4. Proietta il QR: gli allievi lo inquadrano, scrivono nome e un codice personale di 4 cifre.

Le istruzioni complete sono nel LEGGIMI.txt dentro lo zip. I progressi fatti con il pacchetto restano sul PC dell'istruttore, non nell'app online.

## Limiti del piano gratuito di Cloudflare

Il limite che conta sono i 50 utenti di Zero Trust; spazio e richieste sono ampi per una classe.

| Cosa | Limite gratuito | Noi oggi |
| --- | --- | --- |
| Utenti che entrano con l'email (Zero Trust) | 50, istruttore compreso | Oltre 50 si paga ogni utente: listino 7 $ al mese ciascuno, annuale |
| File per sito | 20.000 | Circa 1.280 (104 MB) |
| Dimensione di un file | 25 MiB | Il più grande circa 1,9 MB |
| Richieste al Worker | 100.000 al giorno, azzerate alle 2 italiane (1 con l'ora solare) | Le slide e le appendici contano; i file normali no |
| Operazioni sull'archivio dei progressi | 100.000 richieste al giorno | Ogni slide scaricata ne usa una |
| Spazio dell'archivio dei progressi | 5 GB | Pochi MB |

Con 30-40 allievi si resta largamente nei limiti; il momento più pesante è quando tutti scaricano le slide per l'uso offline. Le prove con il link non occupano posti. I numeri cambiano: prima di spendere ricontrolla la pagina dei prezzi.

## Problemi frequenti

| Problema | Soluzione |
| --- | --- |
| «Pagina riservata» o entra con l'email sbagliata | Aprire [la pagina di uscita](https://corsonautico-ondaportante.fafiorucci.workers.dev/cdn-cgi/access/logout), poi di nuovo il link del corso con l'email giusta |
| Il codice per email non arriva | Controllare lo spam; se non arriva, l'email non è nella policy «Allievi» |
| «Accesso da rinnovare» | Sessione scaduta o email tolta: rientrare con il codice, o riaggiungere l'email |
| L'area istruttore non si trova | L'indirizzo finisce con /docente, per intero |
| Novità dell'app non visibili | Chiudere e riaprire l'app due volte |
| La demo dallo zip dice che non carica il corso | Scompattare tutta la cartella e aprire index.html da lì |
| Una lezione ha il lucchetto | Aprirla dall'area istruttore, scheda «Lezioni» |

## Fonti

Documentazione di Cloudflare consultata il 9 ottobre 2026.

- [Seat management · Cloudflare One](https://developers.cloudflare.com/cloudflare-one/team-and-resources/users/seat-management/)
- [Limiti dei Workers](https://developers.cloudflare.com/workers/platform/limits/)
- [Prezzi dei Workers](https://developers.cloudflare.com/workers/platform/pricing/)
- [Limiti dei Durable Objects](https://developers.cloudflare.com/durable-objects/platform/limits/)
- [Prezzi dei Durable Objects](https://developers.cloudflare.com/durable-objects/platform/pricing/)
- [Cloudflare Access: piani e prezzi](https://www.cloudflare.com/sase/products/access/)

Dettagli tecnici dell'app (per chi la modifica): corso/app/README.md nel repository.
