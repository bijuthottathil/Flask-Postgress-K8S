from flask import Flask, request, jsonify, Response
from db import get_db_connection
import psycopg2.extras
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# 🔢 Prometheus metrics
REQUEST_COUNT = Counter('flask_app_requests_total', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('flask_app_request_latency_seconds', 'Request latency', ['endpoint'])

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    if hasattr(request, 'start_time'):
        resp_time = time.time() - request.start_time
        REQUEST_LATENCY.labels(request.path).observe(resp_time)
        REQUEST_COUNT.labels(request.method, request.path).inc()
    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM items')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO items (name) VALUES (%s)', (data['name'],))
    conn.commit()
    cur.close()
    conn.close()
    return {'message': 'Item added'}, 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)