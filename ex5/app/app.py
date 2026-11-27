import os, psycopg2
from flask import Flask, request, jsonify
app = Flask(__name__)
def get_conn():
    return psycopg2.connect(host=os.getenv("DB_HOST", "db"), dbname=os.getenv("POSTGRES_DB"), user=os.getenv("POSTGRES_USER"), password=os.getenv("POSTGRES_PASSWORD"))
@app.route("/tasks", methods=["GET"])
def list_tasks():
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks ORDER BY id;")
    rows = [{"id": r[0], "title": r[1], "done": r[2]} for r in cur.fetchall()]
    cur.close(); conn.close()
    return jsonify(rows)
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    conn = get_conn(); cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, done;", (data["title"],))
    row = cur.fetchone(); conn.commit(); cur.close(); conn.close()
    return jsonify({"id": row[0], "title": row[1], "done": row[2]}), 201
@app.route("/tasks/<int:tid>/done", methods=["PUT"])
def done_task(tid):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("UPDATE tasks SET done = TRUE WHERE id = %s RETURNING id, title, done;", (tid,))
    row = cur.fetchone(); conn.commit(); cur.close(); conn.close()
    return (jsonify({"id": row[0], "title": row[1], "done": row[2]}), 200) if row else (jsonify({"error": "Not found"}), 404)
@app.route("/tasks/<int:tid>", methods=["DELETE"])
def del_task(tid):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s;", (tid,))
    conn.commit(); cur.close(); conn.close()
    return "", 204
