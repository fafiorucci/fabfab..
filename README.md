# Studio Meteo

Web app meteo in HTML/CSS/JS puro, senza dipendenze né build. Usa le API gratuite di [Open-Meteo](https://open-meteo.com/) (nessuna chiave API richiesta).

## Funzioni

- Ricerca città con suggerimenti (navigabili da tastiera)
- Posizione attuale tramite geolocalizzazione del browser
- Condizioni attuali: temperatura, percepita, umidità, vento, pressione, precipitazioni, indice UV, alba e tramonto
- Grafico delle prossime 24 ore (temperatura e probabilità di pioggia) e lista oraria
- Previsioni a 7 giorni con barre min/max
- Cambio °C / °F; ultima città e unità vengono ricordate
- Tema chiaro/scuro automatico, layout responsive

## Avvio

Apri `index.html` nel browser, oppure servi la cartella:

```sh
python3 -m http.server 8000
# poi apri http://localhost:8000
```

La geolocalizzazione richiede `localhost` o HTTPS. Si può pubblicare così com'è su GitHub Pages.
