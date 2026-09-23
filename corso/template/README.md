# Template delle slide del corso

Vale per tutte le slide del corso «Patente nautica Vela/Motore senza limiti dalla costa» di Fabrizio Fiorucci.
Formato 16:9, 1920×1080.

## Stile (creativo, colorato)

Ispirato ai pannelli illustrati del «Corso di vela · Manovre, condotta e sicurezza», rielaborato.

- **Fondo** crema `#FFF8EE` con forme morbide colorate negli angoli e onde tenui in basso; copertine blu notte `#16324F` con una scena illustrata (sole, nuvole, gabbiani, barca a vela, motoscafo).
- **Intestazioni**: bollino a forma morbida con icona, etichetta a capsula colorata, **titolo colorato** (Fredoka 700, 64 px). I colori ruotano: corallo `#E4572E`, mare `#0B8A99`, viola `#7B5CD6`, blu `#2F6FDB`, verde `#2E9E5B`; giallo sole `#F4A300` per gli accenti.
- **Schede** bianche con barretta colorata a sinistra e ombra morbida (raggio 28 px); schede tinte per i riquadri di carteggio (`#D5F3F5`).
- **Disegni** su pannelli arrotondati verde mare `#E4F3F1` con onde disegnate; carena rossa antivegetativa, linea di galleggiamento blu, scafi bianchi con contorno blu notte.
- **Caratteri**: Fredoka (titoli), Nunito Sans (testo), Caveat (note scritte a mano).
- **Grafici**: coppia validata `#008C9E` (carta 5/D) e `#C0582C` (carta 42/D).

Tutto è in `template.py`; `anteprima.py` genera un'immagine di controllo delle slide.

## Impaginazione

- Margini 128 px; in basso 160 px per lasciare spazio al piè di pagina.
- Occhiello in maiuscolo sopra il titolo (es. «Lezione 03 · 2 ore»).
- Contenuti in riquadri affiancati con angoli arrotondati (16 px).

## Elementi fissi su ogni slide

1. **Sfondo marino** (`sfondo-chiaro.svg` / `sfondo-scuro.svg`, generati da `sfondo.py`): rosa dei venti in filigrana in alto a destra e onde tenui lungo il bordo basso. Va messo come primo elemento della slide, a tutta pagina.
2. **Piè di pagina a sinistra**: logo piccolo (48 px, `../logo/logo-fiorucci.svg`, negativo sulle slide scure) e la scritta «Fabrizio Fiorucci · Patente nautica Vela/Motore senza limiti dalla costa».
3. **Numero di pagina** in basso a destra.
4. **Copertina**: logo grande con nome e «Skipper e istruttore di vela» in alto a sinistra.
