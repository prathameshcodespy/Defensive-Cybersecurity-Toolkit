from scanner import scan_ports
from risk_engine import analyze_risks
from report_generator import generate_report
from ai_explainer import explain_risks
from colorama import Fore, init

init(autoreset=True)

def risk_meter(score):
    filled = score // 5
    empty = 20 - filled
    bar = "█" * filled + "░" * empty
    print(f"\nRisk Level: [{bar}] {score}/100")

def main():
    print(Fore.MAGENTA + """
===========================================
 DEFENSIVE CYBERSECURITY TOOLKIT v1.0
===========================================
""")

    target = input(Fore.YELLOW + "Enter target IP: ")
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    # Scan ports
    open_ports = scan_ports(target, start_port, end_port)

    print(Fore.CYAN + "\nScan Results:")
    print(open_ports)

    # Show open ports properly
    if open_ports:
        print(Fore.RED + f"\nOpen Ports Found: {len(open_ports)}")
        for port in open_ports:
            print(Fore.RED + f"Port {port} is OPEN")
    else:
        print(Fore.GREEN + "\nNo open ports detected. System appears secure.")

    # Analyze risks
    risks = analyze_risks(open_ports)
    total_score = sum(r["score"] for r in risks)

    if total_score > 100:
        total_score = 100
        if total_score <= 20:
            grade = "A"
    elif total_score <= 40:
        grade = "B"
    elif total_score <= 60:
        grade = "C"
    elif total_score <= 80:
        grade = "D"
    else:
        grade = "F"

    print(Fore.CYAN + f"Compliance Grade: {grade}")



    if risks:
        print(Fore.RED + "\n⚠ RISKS DETECTED:")

    # 🔥 Overall Risk Score Display
    print(Fore.MAGENTA + f"\nOverall Risk Score: {total_score}/100")

    # 🔥 Individual Risk Details
    for r in risks:
        if r["severity"] == "CRITICAL":
            color = Fore.RED
        elif r["severity"] == "MEDIUM":
            color = Fore.YELLOW
        else:
            color = Fore.GREEN

        print(color + f"""
Port: {r['port']}
Severity: {r['severity']}
Risk Score: {r['score']}
Issue: {r['description']}
CVE Reference: {r['cve']}
""")

    explanations = explain_risks(risks)

    if explanations:
        print(Fore.YELLOW + "\nAI Risk Explanation:")
        for e in explanations:
            print(e)

    else:
        print(Fore.GREEN + "\nNo major risks detected.")



        # AI explanation only if risks exist
    explanations = explain_risks(risks)

    if explanations:
            print(Fore.YELLOW + "\nAI Risk Explanation:")
            for e in explanations:
                print(e)
    else:
        print(Fore.GREEN + "\nNo major risks detected.")

    # Generate report
    report = generate_report(target, open_ports, risks)
    print(Fore.BLUE + f"\nReport saved as {report}")


if __name__ == "__main__":
    main()
