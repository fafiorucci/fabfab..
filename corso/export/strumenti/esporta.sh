#!/bin/bash
# Esporta uno o più deck scaricati in corso/export/{html,pdf,pptx}.
# uso: esporta.sh <cartella_deck> [<cartella_deck> ...]
# ogni cartella contiene project/deck.json e project/slides/*.html (scaricati dall'artifact)
set -e
QUI=$(cd "$(dirname "$0")" && pwd)
OUT=$(cd "$QUI/.." && pwd)
for d in "$@"; do
  n=$(python3 -c "
import json,sys;t=json.load(open(sys.argv[1]+'/project/deck.json'))['title']
print(t.replace(' · ',' - ').replace('/','-').replace(':','').replace('?',''))" "$d")
  python3 "$QUI/export.py" "$d" "$n" "$OUT"
done
