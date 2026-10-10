#!/bin/sh
# Tiene "caldi" i dati che l'app chiede più spesso: griglia della zona, modelli principali, onda, carte sinottiche.
MODELLI="ecmwf_ifs025,gfs_seamless,icon_seamless,meteofrance_seamless,ukmo_seamless,italia_meteo_arpae_icon_2i"
SINOTTICA="ecmwf_ifs025,gfs_seamless,icon_seamless,ukmo_seamless,meteofrance_seamless,gem_seamless,ecmwf_aifs025_single"
set -- $ZONA
W=$1; S=$2; E=$3; N=$4

# Elenco dei punti della griglia, a blocchi di 200 (latitudini;longitudini)
blocchi() {
  awk -v w="$1" -v s="$2" -v e="$3" -v n="$4" -v p="$5" 'BEGIN {
    c = 0; la = ""; lo = "";
    for (y = s; y <= n + 1e-9; y += p) for (x = w; x <= e + 1e-9; x += p) {
      la = la (c ? "," : "") y; lo = lo (c ? "," : "") x; c++;
      if (c == 200) { print la ";" lo; c = 0; la = ""; lo = "" }
    }
    if (c) print la ";" lo
  }'
}

chiedi() { # $1 = descrizione, $2 = url
  t0=$(date +%s)
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 1800 "$2")
  echo "$(date '+%d/%m %H:%M') $1: HTTP $code in $(( $(date +%s) - t0 )) s"
}

sleep 20
while true; do
  echo "--- riscaldamento $(date '+%d/%m %H:%M') ---"
  # 1) zona abituale a maglia fine: prepara anche i modelli ad alta risoluzione (AROME, ICON-2I, ICON-D2)
  if [ -n "$ZONA_FINE" ]; then
    set -- $ZONA_FINE
    blocchi "$1" "$2" "$3" "$4" "${PASSO_FINE:-0.1}" | while IFS=';' read -r LA LO; do
      chiedi "zona fine: vento" "$SERVER/v1/forecast?latitude=$LA&longitude=$LO&hourly=wind_speed_10m,wind_direction_10m,wind_gusts_10m&models=$MODELLI&forecast_days=7"
      chiedi "zona fine: onda" "$SERVER/v1/marine?latitude=$LA&longitude=$LO&hourly=wave_height,wave_direction,wave_period,swell_wave_height&forecast_days=7"
    done
  fi
  # 2) zona ampia a maglia larga
  blocchi "$W" "$S" "$E" "$N" "$PASSO" | while IFS=';' read -r LA LO; do
    chiedi "vento e pressione" "$SERVER/v1/forecast?latitude=$LA&longitude=$LO&hourly=wind_speed_10m,wind_direction_10m,wind_gusts_10m&models=$MODELLI&forecast_days=7"
    chiedi "pressione e pioggia" "$SERVER/v1/forecast?latitude=$LA&longitude=$LO&hourly=pressure_msl,precipitation&models=$MODELLI&forecast_days=7"
    chiedi "onda" "$SERVER/v1/marine?latitude=$LA&longitude=$LO&hourly=wave_height,wave_direction,wave_period,swell_wave_height&forecast_days=7"
  done
  blocchi -30 24 42 66 3 | while IFS=';' read -r LA LO; do
    chiedi "carte sinottiche" "$SERVER/v1/forecast?latitude=$LA&longitude=$LO&hourly=pressure_msl&models=$SINOTTICA&timezone=GMT&past_days=1&forecast_days=6"
  done
  sleep $(( ${OGNI_MINUTI:-60} * 60 ))
done
