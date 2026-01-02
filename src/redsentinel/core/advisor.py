"""
AI-style security advisor
"""

from redsentinel.core.state import STATE


def security_advice():
    if not STATE["risk"]:
        print("[!] No risk data available.")
        return

    print("[+] AI Security Advisor\n")

    for vuln, data in STATE["risk"].items():
        if data["score"] >= 7:
            print(
                f"- PRIORITY FIX: {vuln}\n"
                f"  Recommendation: Patch immediately, apply hardening, "
                f"and monitor for exploitation attempts.\n"
            )
        elif data["score"] >= 5:
            print(
                f"- {vuln}\n"
                f"  Recommendation: Schedule remediation and improve monitoring.\n"
            )
        else:
            print(
                f"- {vuln}\n"
                f"  Recommendation: Low risk, fix during routine maintenance.\n"
            )

