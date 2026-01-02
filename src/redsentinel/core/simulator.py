# ============================================================
# src/redsentinel/core/simulator.py
# ============================================================
"""
RedSentinel Simulator – LIVE TOOL EXECUTION
------------------------------------------
This version ACTUALLY runs:
- ping
- nmap
- whatweb
- nikto

Then:
- parses raw output into findings
- assigns CVSS severity
- ALWAYS generates HTML + PDF when findings exist

⚠️ Run ONLY on targets you own or have permission to test.
"""

import subprocess
import os
from dataclasses import dataclass, field
from typing import Dict, List

from redsentinel.core.cvss import assign_severity
from redsentinel.core.html_reporter import generate_html_report
from redsentinel.core.pdf_reporter import generate_pdf_report
from redsentinel.core.risk_heatmap import generate_risk_heatmap


# =========================
# State container
# =========================

@dataclass
class SimulationState:
    target: str
    findings: Dict[str, List[dict]] = field(default_factory=dict)
    heatmap: str | None = None
    html_report: str | None = None
    pdf_report: str | None = None


# =========================
# Command runner
# =========================

def run_cmd(cmd: list[str], timeout: int = 120) -> str:
    try:
        res = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout
        )
        return res.stdout
    except Exception as e:
        return f"[ERROR] {e}"


# =========================
# Tool wrappers
# =========================

def run_ping(target: str) -> str:
    return run_cmd(["ping", "-c", "3", target], timeout=20)


def run_nmap(target: str) -> str:
    return run_cmd(["nmap", "-Pn", "-F", target])


def run_whatweb(target: str) -> str:
    return run_cmd(["whatweb", target])


def run_nikto(target: str) -> str:
    return run_cmd(["nikto", "-h", target])


# =========================
# Naive parsers (expandable)
# =========================

def parse_output(tool: str, output: str) -> List[str]:
    findings = []
    for line in output.splitlines():
        l = line.lower()
        if any(x in l for x in [
            "open", "missing", "not present",
            "disallowed", "vulnerable", "exposed",
            "x-frame-options", "x-content-type",
        ]):
            findings.append(f"{tool}: {line.strip()}")
    return findings


# =========================
# Main simulation
# =========================

def simulate_scan(target: str) -> SimulationState:
    print(f"\n[+] Running live security scan against: {target}\n")

    state = SimulationState(target=target)

    raw_findings: Dict[str, List[str]] = {}

    # ---- Run tools ----
    raw_findings["ping"] = parse_output("ping", run_ping(target))
    raw_findings["nmap"] = parse_output("nmap", run_nmap(target))
    raw_findings["whatweb"] = parse_output("whatweb", run_whatweb(target))
    raw_findings["nikto"] = parse_output("nikto", run_nikto(target))

    # ---- Remove empty sections ----
    raw_findings = {k: v for k, v in raw_findings.items() if v}

    if not raw_findings:
        print("[!] No findings detected by tools")
        return state

    # ---- Enrich with CVSS ----
    enriched: Dict[str, List[dict]] = {}

    for source, items in raw_findings.items():
        enriched[source] = []
        for item in items:
            severity, score = assign_severity(item)
            enriched[source].append({
                "data": item,
                "severity": severity,
                "cvss": score,
            })

    state.findings = enriched

    # ---- Reports ----
    os.makedirs("reports", exist_ok=True)

    state.heatmap = generate_risk_heatmap(enriched, output_dir="reports")

    state.html_report = generate_html_report(
        target=target,
        findings=enriched,
        heatmap_path=state.heatmap,
    )

    state.pdf_report = generate_pdf_report(state.html_report)

    print("[+] HTML report generated:", state.html_report)
    print("[+] PDF report generated:", state.pdf_report)

    return state

