import os
import mysql.connector
from flask import Flask, request, redirect
from markupsafe import escape

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
    )


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS messages ("
        "id INT AUTO_INCREMENT PRIMARY KEY, "
        "name VARCHAR(100), "
        "message TEXT, "
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name, message FROM messages ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    form = """
    <h1>Guestbook</h1>
    <form method="post" action="/add">
      <input name="name" placeholder="Your name" required><br>
      <textarea name="message" placeholder="Your message" required></textarea><br>
      <button type="submit">Submit</button>
    </form>
    <hr>
    """
    items = "<br>".join(
        f"<b>{escape(name)}</b>: {escape(message)}" for name, message in rows
    )
    return form + items


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    message = request.form["message"]
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (name, message) VALUES (%s, %s)", (name, message)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)