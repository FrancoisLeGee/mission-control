#!/bin/bash
# Mission Control Pro — Auto-Launch (no wizard)
export OPENCLAW_GATEWAY_URL="ws://127.0.0.1:18789"
export OPENCLAW_AUTH_TOKEN="7ae1dcd50ef59eb7799c629c9899fad4d212d7d38316d8a5"
export PORT=3000
export HOSTNAME="0.0.0.0"

# Prüfe ob schon läuft
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null | grep -q 200; then
    xdg-open http://localhost:3000
    exit 0
fi

# Starte Mission Control
cd /home/francois/mission-control-app
npx next start --port 3000 &

# Warte bis bereit
for i in {1..15}; do
    sleep 2
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null | grep -q 200; then
        xdg-open http://localhost:3000
        exit 0
    fi
done
xdg-open http://localhost:3000
