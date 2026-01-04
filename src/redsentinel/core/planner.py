"""
planner.py
----------
Handles planning logic for RedSentinel.

There are TWO types of plans:
1. Attack Plan      → What to test (no scanning)
2. Remediation Plan → How to fix findings (from reports)
"""

from redsentinel.core.state import STATE


# =====================================================
# ATTACK PLAN (PRE-ENGAGEMENT / RED TEAM STYLE)
# =====================================================

def generate_attack_plan(target: str, framework: str = "generic") -> list:
    """
    Generate an attack / engagement plan for a given target.
    This does NOT run scans and does NOT require prior results.
    """

    print(f"\n[+] Generating attack plan for: {target}")
    print(f"[+] Framework: {framework}\n")

    plan = []

    # ---------------- GENERIC RECON ----------------
    plan.append("Perform DNS enumeration")
    plan.append("Identify IP address and hosting provider")
    plan.append("Run TCP and UDP port scanning")
    plan.append("Enumerate web technologies and HTTP headers")

    # ---------------- WEB ATTACK SURFACE ----------------
    plan.append("Check for missing security headers")
    plan.append("Enumerate directories and files")
    plan.append("Identify exposed admin or debug endpoints")
    plan.append("Test authentication and authorization logic")

    # ---------------- CREDENTIAL & ACCESS ----------------
    plan.append("Assess brute-force protection mechanisms")
    plan.append("Test for default or weak credentials")
    plan.append("Analyze login and error responses")

    # ---------------- POST-ENUM (SAFE) ----------------
    plan.append("Passively identify potential vulnerabilities")
    plan.append("Map findings to MITRE ATT&CK techniques")

    STATE["target"] = target
    STATE["attack_plan"] = plan

    print("[+] Attack plan generated:\n")
    for step in plan:
        print(f" - {step}")

    return plan


# =====================================================
# REMEDIATION PLAN (POST-SCAN / BLUE TEAM STYLE)
# =====================================================

def generate_remediation_plan(report: dict) -> list:
    """
    Generate remediation steps based on scan findings.
    Requires an existing scan report.
    """

    plan = []
    findings = report.get("findings", {})

    if not findings:
        return [{
            "severity": "INFO",
            "issue": "No findings detected",
            "recommendation": "No remediation required"
        }]

    for tool, items in findings.items():
        for item in items:
            severity = item.get("severity", "INFO")
            issue = item.get("data", "Unknown issue")

            recommendation = _recommendation_from_severity(severity)

            plan.append({
                "tool": tool,
                "severity": severity,
                "issue": issue,
                "recommendation": recommendation
            })

    STATE["remediation_plan"] = plan
    return plan


def _recommendation_from_severity(severity: str) -> str:
    severity = severity.upper()

    if severity == "CRITICAL":
        return "Immediately patch affected services and restrict exposure."
    if severity == "HIGH":
        return "Apply security updates and review service configuration."
    if severity == "MEDIUM":
        return "Harden configuration and enable monitoring."
    if severity == "LOW":
        return "Fix when possible to improve security posture."
    return "Informational finding. No immediate action required."

