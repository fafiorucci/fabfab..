# Lezione 10 · Carteggio: navigazione costiera (carta 5/D)

Slide (artifact Slides): https://claude.ai/artifact/64DeNcgDYeo8AtFEnDjbqG

65 slide. Le 26 prove ufficiali delle famiglie 5.1.3, 5.2.3, 5.3.3 e 5.4.3 (DD 131/2022), ciascuna con una
slide per la traccia (carta senza soluzione) e una per il tracciamento (carta, passaggi, risultato e risposta ufficiale).
Prima degli esercizi: le conversioni da usare, le cinque tecniche (rilevamento trasportato sullo stesso punto e su
punti diversi, tre rilevamenti, passaggio al traverso, intercettazione), la tabella di deviazione e un quiz.

- `cart/es10.py`: soluzioni calcolate e confrontate con le risposte ufficiali (`python3 cart/es10.py`).
  23 risultati su 26 cadono dentro la forchetta ufficiale; 5.1.3-6, 5.3.3-6 e 5.4.3-3 la mancano di circa 0,1′
  (la tolleranza di un tracciamento a matita).
- `cart/geo.py`: conversioni, tabella di deviazione dell'Allegato A, punti nave.
- `cart/chart.py`: disegno delle carte schematiche.
- `cart/landmarks.json`: coordinate dei punti cospicui da OpenStreetMap (© contributori OSM, ODbL). Punta Nera
  e Torre di Cala della Ruta sono state ricavate risolvendo al contrario gli esercizi ufficiali.
- La costa (`cart/coast.json`, `cart/coast_rings.json`) viene da OpenStreetMap tramite Overpass. È troppo grande
  per il repository: va riscaricata con la query `natural=coastline` nel riquadro 42,2-43,15 N / 9,7-11,35 E.

Rigenerare: `python3 genera.py`.
