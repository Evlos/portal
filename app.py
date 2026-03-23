import os
import sqlite3
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "bookmarks.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookmarks (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                title   TEXT,
                url     TEXT NOT NULL,
                sort_order INTEGER DEFAULT 0
            )
        """)
        conn.commit()

@app.route("/")
def index():
    with get_db() as conn:
        items = conn.execute(
            "SELECT * FROM bookmarks ORDER BY sort_order ASC, id ASC"
        ).fetchall()
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    url   = request.form.get("url", "").strip()
    if not url:
        return redirect(url_for("index"))
    with get_db() as conn:
        max_order = conn.execute("SELECT MAX(sort_order) FROM bookmarks").fetchone()[0]
        next_order = (max_order or 0) + 1
        conn.execute(
            "INSERT INTO bookmarks (title, url, sort_order) VALUES (?, ?, ?)",
            (title or url, url, next_order)
        )
        conn.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:item_id>", methods=["POST"])
def delete(item_id):
    with get_db() as conn:
        conn.execute("DELETE FROM bookmarks WHERE id = ?", (item_id,))
        conn.commit()
    return jsonify({"status": "ok"})

@app.route("/edit/<int:item_id>", methods=["POST"])
def edit(item_id):
    data  = request.get_json()
    title = (data.get("title") or "").strip()
    url   = (data.get("url")   or "").strip()
    if not url:
        return jsonify({"status": "error", "message": "URL required"}), 400
    with get_db() as conn:
        conn.execute(
            "UPDATE bookmarks SET title = ?, url = ? WHERE id = ?",
            (title or url, url, item_id)
        )
        conn.commit()
    return jsonify({"status": "ok", "title": title or url, "url": url})

@app.route("/reorder", methods=["POST"])
def reorder():
    order = request.get_json()  # list of ids in new order
    with get_db() as conn:
        for idx, item_id in enumerate(order):
            conn.execute(
                "UPDATE bookmarks SET sort_order = ? WHERE id = ?",
                (idx, item_id)
            )
        conn.commit()
    return jsonify({"status": "ok"})

init_db()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
