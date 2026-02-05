from flask import Flask, render_template, request, redirect, session
from scanner import scan_ports
from risk_engine import analyze_risks

app = Flask(__name__)
app.secret_key = "supersecretkey"

USERNAME = "admin"
PASSWORD = "secure123"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect("/")
    return render_template("login.html")

@app.route("/", methods=["GET", "POST"])
def home():
    if not session.get("logged_in"):
        return redirect("/login")

    results = None
    risks = None

    if request.method == "POST":
        target = request.form["target"]

        # Restrict scanning to localhost for safety
        if target != "127.0.0.1":
            return "Demo version allows localhost scanning only."

        start_port = int(request.form["start_port"])
        end_port = int(request.form["end_port"])

        results = scan_ports(target, start_port, end_port)
        risks = analyze_risks(results)

    return render_template("index.html", results=results, risks=risks)

if __name__ == "__main__":
    app.run(debug=True)
    
    @app.route("/logout")   
    def logout():
     session.pop("logged_in", None)
     return redirect("/login")

