#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 update_status.py

git add status.json update_status.py README.md index.html launch.sh launch-pro.sh mission-control.py mission-control.desktop 2>/dev/null || true
if ! git diff --cached --quiet; then
  git commit -m "Update live status" >/dev/null 2>&1 || true
  git push origin main >/dev/null 2>&1 || true
  git push hf main --force >/dev/null 2>&1 || true
fi

echo "Mission Control synced"
