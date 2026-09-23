# Template delle slide del corso

Vale per tutte le slide del corso «Patente nautica Vela/Motore senza limiti dalla costa» di Fabrizio Fiorucci.
Formato 16:9, 1920×1080.

## Colori

| Uso | Colore |
|---|---|
| Fondo chiaro (slide di contenuto) | `#F5F1E8` |
| Fondo scuro (copertina, chiusure) | `#10263A` |
| Riquadri teoria | `#EAE4D6` |
| Riquadri carteggio | `#DCE8E6` |
| Titoli | `#14212E` (su scuro `#F5F1E8`) |
| Testo | `#3A4652` (su scuro `#B9C7D2`) |
| Accento teoria, occhielli | `#A8432A` (su scuro `#E9A07F`) |
| Accento carteggio | `#1F6F78` |
| Piè di pagina | `#5C6874` |

## Caratteri

- Titoli: **Libre Baskerville** 700 (Google Fonts)
- Testo: **Public Sans** 400–700 (Google Fonts)
- Scala: 96 copertina · 64 titoli · 32–36 titoli di riquadro · 24–28 testo · 24 piè di pagina e occhielli

## Impaginazione

- Margini 128 px; in basso 160 px per lasciare spazio al piè di pagina.
- Occhiello in maiuscolo sopra il titolo (es. «Lezione 03 · 2 ore»).
- Contenuti in riquadri affiancati con angoli arrotondati (16 px).

## Elementi fissi su ogni slide

1. **Sfondo marino** (`sfondo-chiaro.svg` / `sfondo-scuro.svg`, generati da `sfondo.py`): rosa dei venti in filigrana in alto a destra e onde tenui lungo il bordo basso. Va messo come primo elemento della slide, a tutta pagina.
2. **Piè di pagina a sinistra**: logo piccolo (48 px, `../logo/logo-fiorucci.svg`, negativo sulle slide scure) e la scritta «Fabrizio Fiorucci · Patente nautica Vela/Motore senza limiti dalla costa».
3. **Numero di pagina** in basso a destra.
4. **Copertina**: logo grande con nome e «Skipper e istruttore di vela» in alto a sinistra.
