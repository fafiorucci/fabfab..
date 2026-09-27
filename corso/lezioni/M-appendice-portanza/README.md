# Appendice M · La portanza

La portanza dall'ala alla vela (33 slide), in cinque parti:

1. **Che cos'è la portanza**: risalire il vento (dai vascelli del '700 a Luna Rossa), portanza e resistenza, la mano fuori dal finestrino, Newton (flusso deviato, F = m·a), Bernoulli (pressioni), il mito del «percorso più lungo».
2. **Come nasce la portanza**: senza viscosità niente portanza (effetto Coandă, l'uovo sotto il rubinetto), il vortice di partenza e la circolazione (Helmholtz), l'effetto Magnus e la nave a rotori di Flettner, il vento che cede energia alla barca.
3. **Da cosa dipende**: angolo di incidenza, stallo, ½ ρ V² S CL.
4. **La vela è un'ala**: pressioni sulla vela, propulsione e scarroccio, la deriva come ala in acqua, resistenza indotta e vortici d'estremità.
5. **In pratica**: portanza e andature, i filetti (lettura e regola barra/ruota), dove mettere i filetti, grasso e magro, la fessura tra fiocco e randa, il cantiere in autostrada, vero o falso tra web e libri.

Tre verifiche con quiz ufficiali di vela (2.1.1, 2.3.1), ognuna seguita dalla slide con le risposte.

## Fonti

- **Laura Romanò, «La fisica in barca a vela», capitolo 4 «La portanza»** (paragrafi 4.1–4.6): fonte principale, citata in fondo a ogni slide che la usa e nelle note del relatore.
- NASA Glenn Research Center, «Incorrect Lift Theory» e «Bernoulli and Newton».
- Arvel Gentry, «A Review of Modern Sail Theory» (effetto fessura, filetti).

## Disegni calcolati

`flow.py` risolve il flusso potenziale attorno a profili di Joukowski con la condizione di Kutta (linee di corrente, pressioni sulla superficie, tempi di percorrenza), più due casi senza condizione di Kutta: la lastra in fluido ideale (circolazione nulla, nessuna portanza) e il cilindro rotante (effetto Magnus). Scrive `flow_lines.json` (servono numpy e matplotlib solo per rigenerarlo). `genera.py` (con `app_common.py`) legge il JSON e produce il mazzo in `deck/project`. Il diagramma dei venti della slide sull'energia è costruito in scala con i vettori dell'esempio del libro.
