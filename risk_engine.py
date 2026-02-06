from cve_lookup import fetch_cves
def analyze_risks(open_ports):
    risks = []

    critical_ports = {
        21: ("FTP - Anonymous access risk", "CVE-1999-0497"),
        23: ("Telnet - Unencrypted remote login", "CVE-2001-0554"),
        445: ("SMB - Vulnerable to ransomware attacks", "CVE-2017-0144")
    }

    medium_ports = {
        80: ("HTTP - Unsecured web traffic", "CVE-2019-11043"),
        443: ("HTTPS - Check SSL configuration", "CVE-2014-0160")
    }

    for port in open_ports:
        if port in critical_ports:
            description, cve = critical_ports[port]
            risks.append({
                "port": port,
                "severity": "CRITICAL",
                "score": 30,
                "description": description,
                "cve": cve
            })
        elif port in medium_ports:
            description, cve = medium_ports[port]
            risks.append({
                "port": port,
                "severity": "MEDIUM",
                "score": 15,
                "description": description,
                "cve": cve
            })
        else:
            risks.append({
                "port": port,
                "severity": "LOW",
                "score": 5,
                "description": "Unknown service - Verify manually",
                "cve": "N/A"
            })

    return risks
