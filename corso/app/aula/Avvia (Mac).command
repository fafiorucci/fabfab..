#!/bin/bash
cd "$(dirname "$0")"
if command -v python3 >/dev/null 2>&1; then python3 server.py; else echo "Serve Python 3: https://www.python.org/downloads/"; open https://www.python.org/downloads/; fi
read -n 1 -s -r -p "Premi un tasto per chiudere"
