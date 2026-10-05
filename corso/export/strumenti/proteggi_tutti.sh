#!/bin/bash
# Protegge tutti i PDF di corso/export/pdf e li scrive in corso/export/pdf-protetti (stesso nome).
# uso: PDF_OWNER_PW='...' strumenti/proteggi_tutti.sh   (password del proprietario: la chiede a Fabrizio)
set -e
QUI=$(cd "$(dirname "$0")" && pwd); OUT=$(cd "$QUI/.." && pwd)
[ -n "$PDF_OWNER_PW" ] || { echo "manca PDF_OWNER_PW"; exit 1; }
mkdir -p "$OUT/pdf-protetti"
for f in "$OUT"/pdf/*.pdf; do
  python3 "$QUI/proteggi.py" "$f" "$OUT/pdf-protetti/$(basename "$f")" "$PDF_OWNER_PW" >/dev/null
  echo "protetto: $(basename "$f")"
done
