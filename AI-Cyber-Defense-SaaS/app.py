from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
scheduler.start()
from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies
)
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import timedelta

app = Flask(__name__)

# ---------------- JWT CONFIG ----------------

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'
app.config['MAIL_DEFAULT_SENDER'] = 'AI Cyber Defense <your_email@gmail.com>'

mail = Mail(app)

def send_email(to, subject, body):
    msg = Message(subject, recipients=[to])
    msg.body = body
    mail.send(msg)
    
def trial_reminder():
    print("Checking trial expirations...")
    # In real SaaS: check DB for expiring users
    # Then send reminder email
    scheduler.add_job(trial_reminder, 'interval', hours=24)
    

app.config["JWT_SECRET_KEY"] = "super_secret_cyber_key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

# IMPORTANT FOR UI MODE
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)

DATABASE = "users.db"

# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- UI ROUTES ----------------

@app.route("/api/admin/broadcast", methods=["POST"])
@jwt_required()
def broadcast():
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"msg": "Admins only"}), 403

    data = request.json
    subject = data["subject"]
    message = data["message"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    conn.close()

    for user in users:
        send_email(user[0] + "@example.com", subject, message)

    return jsonify({"msg": "Broadcast sent"})

@app.route("/")
def home():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = generate_password_hash(request.form.get("password"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
    except:
        conn.close()
        return render_template("register.html", error="User already exists")

    conn.close()
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user or not check_password_hash(user[0], password):
        return render_template("login.html", error="Invalid credentials")

    access_token = create_access_token(
        identity=username,
        additional_claims={"role": user[1]}
    )
    refresh_token = create_refresh_token(identity=username)

    response = make_response(redirect("/dashboard"))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@app.route("/logout")
def logout():
    response = make_response(redirect("/login"))
    unset_jwt_cookies(response)
    return response


# ---------------- PROTECTED UI ----------------

@app.route("/dashboard")
@jwt_required(locations=["cookies"])
def dashboard_page():
    current_user = get_jwt_identity()
    return render_template("dashboard.html", user=current_user)


@app.route("/admin")
@jwt_required(locations=["cookies"])
def admin_page():
    claims = get_jwt()

    if claims["role"] != "admin":
        return redirect("/dashboard")

    return render_template("admin.html")


# ---------------- API ENDPOINTS (OPTIONAL) ----------------

    send_email(
    to=username + "@example.com",  # replace with real email field later
    subject="🚀 Welcome to AI Cyber Defense",
    body="""
Welcome to AI Cyber Defense Platform!

Your 7-day free trial has started.

Start scanning now:
http://127.0.0.1:5000/login

– AI Cyber Team
"""
)

@app.route("/api/dashboard")
@jwt_required()
def dashboard_api():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Welcome {current_user}"})


@app.route("/api/admin")
@jwt_required()
def admin_api():
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"msg": "Admins only"}), 403
    return jsonify({"msg": "Welcome Admin"})


if __name__ == "__main__":
    app.run()
