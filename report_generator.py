from datetime import datetime

def generate_report(target, open_ports, risks):
    filename = "security_audit_report.txt"
    
    with open(filename, "w") as f:
        f.write("=== Defensive Cybersecurity Audit Report ===\n")
        f.write(f"Target: {target}\n")
        f.write(f"Scan Time: {datetime.now()}\n\n")

        f.write("Open Ports:\n")
        for port, service in open_ports:
            f.write(f"- Port {port} ({service})\n")

        f.write("\nRisk Assessment:\n")
        if risks:
            for port, service, reason in risks:
                f.write(f"- Port {port} ({service}) -> {reason}\n")
        else:
            f.write("No high-risk ports detected.\n")

        f.write("\nSecurity Recommendations:\n")
        f.write("- Close unnecessary ports\n")
        f.write("- Use firewall rules\n")
        f.write("- Enable encryption protocols\n")

    return filename
