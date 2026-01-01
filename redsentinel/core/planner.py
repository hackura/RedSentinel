from redsentinel.core.state import STATE


def generate_plan(target: str, framework: str = "generic"):
    """
    Generate a red team / pentest plan for a given target.
    Framework can be: generic, mitre, owasp (future use)
    """

    print(f"\n[+] Generating attack plan for: {target}")
    print(f"[+] Framework: {framework}\n")

    plan = []

    # ---------------- GENERIC RECON ----------------
    plan.append("Perform DNS enumeration")
    plan.append("Identify IP address and hosting provider")
    plan.append("Run port scanning (TCP/UDP)")
    plan.append("Enumerate web technologies and headers")

    # ---------------- WEB ATTACK SURFACE ----------------
    plan.append("Check for missing security headers")
    plan.append("Test authentication endpoints")
    plan.append("Check for exposed admin panels")
    plan.append("Enumerate directories and files")

    # ---------------- CREDENTIAL & ACCESS ----------------
    plan.append("Assess brute-force protections")
    plan.append("Test for default credentials")
    plan.append("Analyze login error messages")

    # ---------------- POST-ENUM (SAFE) ----------------
    plan.append("Identify potential vulnerabilities (passive)")
    plan.append("Map findings to MITRE ATT&CK techniques")

    STATE["target"] = target
    STATE["plan"] = plan

    print("[+] Attack plan generated:\n")
    for step in plan:
        print(f" - {step}")

