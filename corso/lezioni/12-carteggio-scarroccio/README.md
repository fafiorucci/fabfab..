# Lezione 12 · Carteggio: lo scarroccio (carte 5/D e 42/D)

Slide (artifact Slides): https://claude.ai/artifact/Y86JJdezDF7GdAPJPXaR7Q

58 slide. Le 24 prove ufficiali 5.1.4-5.4.4 (carta 5/D) e 5.5.4-5.8.4 (carta 42/D), con traccia e tracciamento.
Prima degli esercizi: i nomi dei venti, la regola Rv = Pv + Sc e il suo segno, il traverso misurato dalla prora
(il punto sta sulla rotta), i conti tra prora, rotta e velocità, un quiz e la carta 42/D.

- `cart/es12.py`: soluzioni e controllo con le risposte ufficiali (`python3 cart/es12.py`): 22 su 24 dentro la forchetta.
  5.3.4-1 dipende dal limite della zona 2 di Montecristo stampato sulla carta (qui un cerchio approssimato, scarto 0,1′);
  5.4.4-4 esce di circa 1′ in longitudine (posizione di Punta Lividonia sulla carta).
- Convenzioni ricavate dagli esercizi ufficiali: «sul rilevamento X del faro a d miglia» significa che dalla barca
  si vede il faro per X; «a d miglia a Nord-Ovest del faro» significa che la barca sta a NW del faro.
- `cart/build_coast.py`: costruisce i poligoni di terra della 42/D dalla costa OSM
  (`python3 cart/build_coast.py coast42.json coast42_rings.json 40.65 8.3 41.6 10.0`).

Rigenerare: `python3 genera.py`.
