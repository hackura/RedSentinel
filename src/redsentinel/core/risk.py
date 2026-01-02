"""
Risk assessment engine (simple CVSS-like logic)
"""

from redsentinel.core.state import STATE


def assess_risk():
    if not STATE["vulnerabilities"]:
        print("[!] No vulnerabilities to assess.")
        return

    print("[+] Assessing risk levels...\n")

    for vuln in STATE["vulnerabilities"]:
        severity = vuln.get("severity", "low")

        score = {
            "low": 2.5,
            "medium": 5.0,
            "high": 7.5,
            "critical": 9.5
        }.get(severity, 2.5)

        STATE["risk"][vuln["name"]] = {
            "severity": severity.upper(),
            "score": score
        }

        print(f"- {vuln['name']}: {severity.upper()} ({score})")

