from flask import Flask, render_template, request, jsonify, redirect, session
import sqlite3
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from openai import OpenAI

# LOAD ENV
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# OPENAI CLIENT
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# DB INIT
def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        phone TEXT,
        address TEXT,
        city TEXT,
        country TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# HOME
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html", user=session["user"])

# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["fullname"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",
                        (name, email, password))
            conn.commit()
        except:
            return "User already exists"

        conn.close()
        return redirect("/login")

    return render_template("signup.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session["user"] = email
            session["conversation"] = [{"role": "system", "content": "You are MediMate AI"}]
            return redirect("/")
        else:
            return "Invalid login"

    return render_template("login.html")

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# PROFILE
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (session["user"],))
    user = cur.fetchone()
    conn.close()

    return render_template("profile.html", user=user)

# SAVE PROFILE
@app.route("/save_profile", methods=["POST"])
def save_profile():
    if "user" not in session:
        return redirect("/login")

    data = request.form
    file = request.files.get("photo")

    if file and file.filename != "":
        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
        UPDATE users SET
        name=?, phone=?, address=?, city=?, country=?
        WHERE email=?
    """, (
        data.get("name"),
        data.get("phone"),
        data.get("address"),
        data.get("city"),
        data.get("country"),
        session["user"]
    ))

    conn.commit()
    conn.close()

    return redirect("/profile")

# CHAT
@app.route("/chat", methods=["POST"])
def chat():
    if "user" not in session:
        return jsonify({"reply": "Login required"})

    msg = request.json["message"]

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO chats(user,message) VALUES(?,?)",
                (session["user"], msg))
    conn.commit()
    conn.close()

    conversation = session.get("conversation", [])
    conversation.append({"role": "user", "content": msg})

    response = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct",
        messages=conversation
    )

    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})

    session["conversation"] = conversation

    return jsonify({"reply": reply})

# GET CHATS
@app.route("/get_chats")
def get_chats():
    if "user" not in session:
        return jsonify([])

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT message FROM chats 
        WHERE user=? ORDER BY id DESC LIMIT 10
    """, (session["user"],))

    chats = cur.fetchall()
    conn.close()

    return jsonify([c[0] for c in chats])

# UPDATE PASSWORD
@app.route("/update_password", methods=["POST"])
def update_password():
    if "user" not in session:
        return redirect("/login")

    current = request.form["current"]
    new = generate_password_hash(request.form["new"])

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE email=?", (session["user"],))
    old = cur.fetchone()[0]

    if not check_password_hash(old, current):
        return "Wrong password"

    cur.execute("UPDATE users SET password=? WHERE email=?", (new, session["user"]))
    conn.commit()
    conn.close()

    return redirect("/profile")

if __name__ == "__main__":
    app.run(debug=True)