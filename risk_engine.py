RISKY_PORTS = {
    21: "FTP - Often insecure without encryption",
    23: "Telnet - Transmits data in plaintext",
    445: "SMB - Common attack vector",
    3389: "RDP - Target for brute force attacks"
}

def analyze_risks(open_ports):
    risks = []
    for port, service in open_ports:
        if port in RISKY_PORTS:
            risks.append((port, service, RISKY_PORTS[port]))
    return risks
