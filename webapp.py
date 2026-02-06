from flask import Flask, render_template, request
from scanner import scan_ports
from risk_engine import analyze_risks

app = Flask(__name__)

def calculate_grade(score):
    if score <= 20:
        return "A"
    elif score <= 40:
        return "B"
    elif score <= 60:
        return "C"
    elif score <= 80:
        return "D"
    else:
        return "F"


@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        target = request.form["target"]
        start_port = int(request.form["start"])
        end_port = int(request.form["end"])

        open_ports = scan_ports(target, start_port, end_port)
        risks = analyze_risks(open_ports)

        total_score = sum(r["score"] for r in risks)
        if total_score > 100:
            total_score = 100

        grade = calculate_grade(total_score)

        return render_template(
            "dashboard.html",
            target=target,
            open_ports=open_ports,
            risks=risks,
            score=total_score,
            grade=grade
        )

    return render_template("dashboard.html")
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

