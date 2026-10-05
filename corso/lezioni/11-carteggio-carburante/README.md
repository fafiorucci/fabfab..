# Lezione 11 · Carteggio: carburante e autonomia (carta 5/D)

Slide (artifact Slides): https://claude.ai/artifact/1dsfk73ddAt2WCCwMDhFnJ

95 slide. Le 23 prove ufficiali delle famiglie 5.1.2, 5.2.2, 5.3.2 e 5.4.2 (DD 131/2022), ciascuna con una slide
per la traccia e una per il tracciamento. Prima degli esercizi: il conto del carburante (tempo, consumo, riserva del 30%),
il doppio rilevamento 45°-90°, la velocità ricavata dalla carta, il punto da rilevamento e distanza e la mappa.

Struttura: 5 capitoli in 75 minuti, ognuno aperto da una slide di apertura e chiuso da una verifica
da 2 quiz ufficiali con la slide delle risposte; negli ultimi 45 minuti la raccolta di 36 quiz ufficiali (1.2.3, 1.7.5 e 1.7.1)
in 12 slide da 3, ognuna seguita dalle risposte (`apertura.py`, `esame.py`, `schema_cart.py`).

- `cart/es11.py`: soluzioni calcolate e confrontate con le risposte ufficiali (`python3 cart/es11.py`). 19 su 23
  dentro la forchetta; 5.3.2-6, 5.4.2-2, 5.4.2-3 e 5.4.2-4 escono di pochissimo (0,1-1 litro), perché la velocità
  ricavata dipende dalla distanza al traverso misurata sulla carta: le slide lo segnalano.
- Gli altri file in `cart/` e la costa OpenStreetMap: come nella lezione 10.

Rigenerare: `python3 genera.py`.
