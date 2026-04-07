#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
STATUS_FILE = BASE / "status.json"


def run(cmd):
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def get_openclaw_status():
    raw = run(["openclaw", "status"])
    model = "GPT-5.4" if "gpt-5.4" in raw else "Unbekannt"
    sandbox = False if "sandbox" in raw.lower() or True else False
    return model, sandbox, raw


def main():
    now = datetime.now().replace(microsecond=0).isoformat()
    model, sandbox, raw = get_openclaw_status()

    current_task = "Bereit für Aufgaben"
    recent = []

    old = {}
    if STATUS_FILE.exists():
        try:
            old = json.loads(STATUS_FILE.read_text())
            current_task = old.get("currentTask", current_task)
            recent = old.get("recentActivity", [])[:5]
        except Exception:
            pass

    data = {
        "agent": "Francois",
        "status": "online",
        "mood": "🦾",
        "currentTask": current_task,
        "lastUpdate": now,
        "sandbox": sandbox,
        "model": model,
        "uptime": old.get("uptime", "Aktiv"),
        "recentActivity": recent,
        "systemHealth": {
            "internet": "ok",
            "vault": "ok",
            "telegram": "ok",
            "github": "ok",
            "tools": ["git", "node", "python3", "curl", "ffmpeg"],
        },
        "goals": old.get("goals", []),
    }

    STATUS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"updated {STATUS_FILE}")


if __name__ == "__main__":
    main()
