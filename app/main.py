from flask import Flask, request, jsonify
from db import get_db_connection
import psycopg2.extras

app = Flask(__name__)

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
