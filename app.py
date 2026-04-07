import json
from pathlib import Path
from flask import Flask, jsonify, send_from_directory

BASE = Path(__file__).parent
app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/')
def root():
    return send_from_directory(BASE, 'index.html')


@app.route('/index.html')
def index_html():
    return send_from_directory(BASE, 'index.html')


@app.route('/status.json')
def status_json():
    path = BASE / 'status.json'
    if path.exists():
        return jsonify(json.loads(path.read_text()))
    return jsonify({'status': 'offline', 'currentTask': 'status.json fehlt'}), 404


@app.route('/<path:path>')
def static_proxy(path):
    target = BASE / path
    if target.exists() and target.is_file():
        return send_from_directory(BASE, path)
    return ('Not found', 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
