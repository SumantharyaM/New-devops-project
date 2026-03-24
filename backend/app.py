from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    host="postgres",
    database="employees",
    user="admin",
    password="admin"
)

@app.route('/')
def home():
    return "App is running!"

@app.route('/add', methods=['POST'])
def add_employee():
    data = request.json
    cur = conn.cursor()
    cur.execute("INSERT INTO emp (name, role) VALUES (%s, %s)", (data['name'], data['role']))
    conn.commit()
    cur.close()
    return "Employee added"

@app.route('/get', methods=['GET'])
def get_employee():
    cur = conn.cursor()
    cur.execute("SELECT * FROM emp")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)

app.run(host='0.0.0.0', port=5000)
