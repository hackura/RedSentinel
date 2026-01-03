import subprocess
import json
from typing import List


# -------------------------
# Nmap
# -------------------------
def run_nmap(target: str) -> List[dict]:
    cmd = ["nmap", "-sV", "--script", "safe", target]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    findings = []
    for line in proc.stdout.splitlines():
        if "/tcp open" in line:
            findings.append({
                "data": line,
                "severity": "MEDIUM",
                "cvss": 5.3,
                "confidence": 0.75
            })
    return findings


# -------------------------
# Nikto
# -------------------------
def run_nikto(target: str) -> List[dict]:
    cmd = ["nikto", "-h", target]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    findings = []
    for line in proc.stdout.splitlines():
        if line.startswith("+"):
            findings.append({
                "data": line,
                "severity": "MEDIUM",
                "cvss": 6.1,
                "confidence": 0.7
            })
    return findings


# -------------------------
# Nuclei
# -------------------------
def run_nuclei(target: str) -> List[dict]:
    cmd = ["nuclei", "-u", target, "-json"]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    findings = []
    for line in proc.stdout.splitlines():
        try:
            obj = json.loads(line)
        except Exception:
            continue

        sev = obj.get("severity", "medium").upper()

        findings.append({
            "data": obj.get("matched-at", target),
            "severity": sev,
            "cvss": severity_to_cvss(sev),
            "confidence": 0.9
        })

    return findings


def severity_to_cvss(sev: str) -> float:
    return {
        "LOW": 3.5,
        "MEDIUM": 6.5,
        "HIGH": 8.5,
        "CRITICAL": 9.8
    }.get(sev, 5.0)
