import json
from pathlib import Path
from flask import Flask, jsonify, Response

BASE = Path(__file__).parent
app = Flask(__name__)


def load_status():
    path = BASE / 'status.json'
    if path.exists():
        return json.loads(path.read_text())
    return {
        'agent': 'Francois',
        'status': 'offline',
        'mood': '⚠️',
        'currentTask': 'status.json fehlt',
        'lastUpdate': '',
        'sandbox': False,
        'model': '—',
        'uptime': '—',
        'recentActivity': [],
        'systemHealth': {},
        'goals': [],
    }


def render_html(d):
    status_class = 'status-online' if d.get('status') == 'online' else 'status-offline'
    dot_class = 'dot-green' if d.get('status') == 'online' else 'dot-red'
    status_text = f"Online {d.get('mood','')}" if d.get('status') == 'online' else 'Offline'
    sandbox_text = '✅ Aktiv' if d.get('sandbox') else '❌ Aus'

    activity_html = ''.join(
        f"<li><span class='activity-time'>{a.get('time','')}</span><span>{a.get('action','')}</span></li>"
        for a in d.get('recentActivity', [])
    ) or '<li>Keine Aktivität</li>'

    health = d.get('systemHealth', {})
    health_html = ''.join(
        f"<div class='health-item'><div class='health-dot health-ok'></div><span>{k}: {v}</span></div>"
        for k, v in health.items() if k != 'tools'
    )
    tools_html = ''.join(
        f"<span class='tool-tag'>{t}</span>" for t in health.get('tools', [])
    )
    goals_html = ''.join(
        f"<li>{g.get('icon','')} {g.get('name','')}</li>" for g in d.get('goals', [])
    )

    return f"""<!DOCTYPE html>
<html lang='de'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>🦾 Francois — Mission Control</title>
<style>
:root {{--bg:#0a0e1a;--card:#131a2e;--border:#1e2a4a;--accent:#4fc3f7;--green:#66bb6a;--red:#ef5350;--text:#e0e6f0;--muted:#7888a0;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Segoe UI',-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:2rem;}}
.header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:2rem;padding-bottom:1rem;border-bottom:1px solid var(--border);}}
.header h1{{font-size:1.8rem;font-weight:600;}}
.header h1 span{{color:var(--accent);}}
.status-badge{{display:inline-flex;align-items:center;gap:.5rem;padding:.4rem 1rem;border-radius:20px;font-size:.85rem;font-weight:600;}}
.status-online{{background:rgba(102,187,106,.15);color:var(--green);border:1px solid rgba(102,187,106,.3);}}
.status-offline{{background:rgba(239,83,80,.15);color:var(--red);border:1px solid rgba(239,83,80,.3);}}
.dot{{width:8px;height:8px;border-radius:50%;animation:pulse 2s infinite;}}
.dot-green{{background:var(--green);}} .dot-red{{background:var(--red);}}
@keyframes pulse{{0%,100%{{opacity:1;}}50%{{opacity:.4;}}}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:1.5rem;}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.5rem;}}
.card h2{{font-size:.85rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin-bottom:1rem;}}
.current-task{{font-size:1.3rem;font-weight:600;color:var(--accent);}}
.task-meta{{margin-top:.5rem;font-size:.85rem;color:var(--muted);}}
.activity-list{{list-style:none;}} .activity-list li{{padding:.6rem 0;border-bottom:1px solid var(--border);display:flex;gap:1rem;font-size:.9rem;}}
.activity-time{{color:var(--accent);font-family:monospace;min-width:3.5rem;}}
.health-grid{{display:grid;grid-template-columns:1fr 1fr;gap:.8rem;}}
.health-item{{display:flex;align-items:center;gap:.5rem;font-size:.9rem;}}
.health-dot{{width:10px;height:10px;border-radius:50%;flex-shrink:0;}} .health-ok{{background:var(--green);}}
.goals-list{{list-style:none;}} .goals-list li{{padding:.5rem 0;font-size:.95rem;display:flex;align-items:center;gap:.5rem;}}
.tools-list{{display:flex;flex-wrap:wrap;gap:.5rem;}} .tool-tag{{background:rgba(79,195,247,.1);border:1px solid rgba(79,195,247,.2);color:var(--accent);padding:.3rem .7rem;border-radius:6px;font-size:.8rem;font-family:monospace;}}
.info-row{{display:flex;justify-content:space-between;padding:.5rem 0;border-bottom:1px solid var(--border);}} .info-row:last-child{{border:none;}} .info-label{{color:var(--muted);}} .info-value{{font-weight:600;}}
.refresh-note{{text-align:center;margin-top:2rem;color:var(--muted);font-size:.8rem;}}
</style>
</head>
<body>
<div class='header'>
<h1>🦾 <span>Francois</span> — Mission Control</h1>
<div class='status-badge {status_class}'><div class='dot {dot_class}'></div><span>{status_text}</span></div>
</div>
<div class='grid'>
<div class='card'><h2>📌 Aktuelle Aufgabe</h2><div class='current-task'>{d.get('currentTask','Nichts gerade')}</div><div class='task-meta'>Letztes Update: {d.get('lastUpdate','—')}</div></div>
<div class='card'><h2>🖥️ System</h2><div class='info-row'><span class='info-label'>Modell</span><span class='info-value'>{d.get('model','—')}</span></div><div class='info-row'><span class='info-label'>Sandbox</span><span class='info-value'>{sandbox_text}</span></div><div class='info-row'><span class='info-label'>Uptime</span><span class='info-value'>{d.get('uptime','—')}</span></div><div class='info-row'><span class='info-label'>Letztes Update</span><span class='info-value'>{d.get('lastUpdate','—')}</span></div></div>
<div class='card'><h2>📋 Letzte Aktivitäten</h2><ul class='activity-list'>{activity_html}</ul></div>
<div class='card'><h2>💚 System Health</h2><div class='health-grid'>{health_html}</div><h2 style='margin-top:1rem;'>🧰 Tools</h2><div class='tools-list'>{tools_html}</div></div>
<div class='card' style='grid-column:1 / -1;'><h2>🎯 Ziele</h2><ul class='goals-list'>{goals_html}</ul></div>
</div>
<div class='refresh-note'>Server-rendered · aktualisiert beim Neuladen</div>
</body>
</html>"""


@app.route('/')
def root():
    return Response(render_html(load_status()), mimetype='text/html')


@app.route('/index.html')
def index_html():
    return Response(render_html(load_status()), mimetype='text/html')


@app.route('/status.json')
def status_json():
    return jsonify(load_status())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
