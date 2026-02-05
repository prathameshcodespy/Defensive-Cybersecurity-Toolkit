from scanner import scan_ports
from risk_engine import analyze_risks
from report_generator import generate_report
from ai_explainer import explain_risks

def main():
    target = input("Enter target IP: ")
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    print("\nScanning...\n")
    open_ports = scan_ports(target, start_port, end_port)

    print("Open Ports:", open_ports)

    risks = analyze_risks(open_ports)

    if risks:
        print("\n⚠ Risks Detected:")
        for r in risks:
            print(r)

        explanations = explain_risks(risks)
        print("\nAI Risk Explanation:")
        for e in explanations:
            print(e)
    else:
        print("\nNo major risks detected.")

    report = generate_report(target, open_ports, risks)
    print(f"\nReport saved as {report}")

if __name__ == "__main__":
    main()
