from flask import Flask, render_template, request, redirect, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import timedelta

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super_secret_cyber_key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

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

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

@app.route("/admin")
def admin_page():
    return render_template("admin.html")

# ---------------- AUTH API ----------------

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = generate_password_hash(data["password"])

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, password))
        conn.commit()
    except:
        return jsonify({"msg": "User already exists"}), 400
    finally:
        conn.close()

    return jsonify({"msg": "Registered successfully"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user or not check_password_hash(user[0], password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username, additional_claims={"role": user[1]})
    refresh_token = create_refresh_token(identity=username)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })


@app.route("/api/dashboard")
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Welcome {current_user}"})


@app.route("/api/admin")
@jwt_required()
def admin():
    claims = get_jwt()
    if claims["role"] != "admin":
        return jsonify({"msg": "Admins only"}), 403
    return jsonify({"msg": "Welcome Admin"})
    

if __name__ == "__main__":
    app.run(debug=True)
