#!/bin/bash
# macOS / Linux launcher -- Vitamin D Ghana Dashboard
cd "$(dirname "$0")"
echo Starting Vitamin D Ghana Dashboard...
python3 app.py &
sleep 1 && open "http://127.0.0.1:8050" 2>/dev/null || xdg-open "http://127.0.0.1:8050"
wait
