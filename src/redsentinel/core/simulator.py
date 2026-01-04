# ============================================================
# src/redsentinel/core/simulator.py
# ============================================================
"""
RedSentinel Simulator – LIVE TOOL EXECUTION
------------------------------------------
Runs:
- ping
- nmap
- whatweb
- nikto
- httpx (json)
- sslscan
- nuclei (json)

Features:
- Proper parsing
- Terminal output
- Confidence scoring
- JSON parsing where supported
- Termux auto-detection
- --no-report CLI flag support
- AI summary with offline fallback
"""

import subprocess
import os
import sys
import json
import shutil
from dataclasses import dataclass, field
from typing import Dict, List

from redsentinel.core.cvss import assign_severity
from redsentinel.core.html_reporter import generate_html_report
from redsentinel.core.pdf_reporter import generate_pdf_report
from redsentinel.core.risk_heatmap import generate_risk_heatmap
from redsentinel.core.normalizer import normalize_findings
from redsentinel.core.ai_interpreter import generate_remediation_roadmap
from redsentinel.core.json_exporter import export_json_report
from redsentinel.core.state import REPORTS_DIR
from redsentinel.core.ai_summary import generate_offline_summary


# =========================
# Termux detection
# =========================

def is_termux() -> bool:
    return "com.termux" in os.environ.get("PREFIX", "").lower()


if is_termux():
    print("[!] Termux detected — ensure tools are installed via pkg / git")
    print("[!] PDF generation may be disabled")


# =========================
# Tool availability
# =========================

def has_tool(cmd: str) -> bool:
    return shutil.which(cmd) is not None


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
    json_report: str | None = None


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
    except Exception:
        return ""


# =========================
# Tool wrappers (HARDENED)
# =========================

def run_ping(target: str) -> str:
    if not has_tool("ping"):
        print("[!] ping skipped (not installed)")
        return ""
    return run_cmd(["ping", "-c", "3", target], timeout=20)


def run_nmap(target: str) -> str:
    if not has_tool("nmap"):
        print("[!] nmap skipped (not installed)")
        return ""
    return run_cmd(["nmap", "-Pn", "-sV", "--script", "safe", target])


def run_whatweb(target: str) -> str:
    if not has_tool("whatweb"):
        print("[!] whatweb skipped (not installed)")
        return ""
    if not has_tool("ruby"):
        print("[!] whatweb skipped (ruby not installed)")
        return ""
    return run_cmd(["whatweb", target])


def run_nikto(target: str) -> str:
    if not has_tool("nikto"):
        print("[!] nikto skipped (not installed)")
        return ""
    if not has_tool("perl"):
        print("[!] nikto skipped (perl not installed)")
        return ""
    return run_cmd(["nikto", "-h", target])


def run_sslscan(target: str) -> str:
    if not has_tool("sslscan"):
        print("[!] sslscan skipped (not installed)")
        return ""
    return run_cmd(["sslscan", target])


def run_httpx_json(target: str) -> List[dict]:
    if not has_tool("httpx"):
        print("[!] httpx skipped (not installed)")
        return []
    try:
        res = subprocess.run(
            ["httpx", "-json", "-tech-detect", "-status-code", "-u", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        return [json.loads(line) for line in res.stdout.splitlines() if line]
    except Exception:
        return []


def run_nuclei_json(target: str) -> List[dict]:
    if not has_tool("nuclei"):
        print("[!] nuclei skipped (not installed)")
        return []
    try:
        res = subprocess.run(
            ["nuclei", "-u", target, "-json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        return [json.loads(line) for line in res.stdout.splitlines() if line]
    except Exception:
        return []


# =========================
# Confidence scoring
# =========================

def calculate_confidence(tool: str, severity: str) -> float:
    base = {
        "CRITICAL": 0.95,
        "HIGH": 0.85,
        "MEDIUM": 0.65,
        "LOW": 0.45,
        "INFO": 0.30
    }.get(severity.upper(), 0.4)

    tool_weight = {
        "nmap": 0.9,
        "nikto": 0.8,
        "whatweb": 0.7,
        "httpx": 0.85,
        "sslscan": 0.8,
        "ping": 0.6,
        "nuclei": 0.95
    }.get(tool.lower(), 0.5)

    return round((base + tool_weight) / 2, 2)


# =========================
# Parsers
# =========================

def parse_output(tool: str, output: str) -> List[str]:
    findings = []

    for line in output.splitlines():
        line = line.strip()
        l = line.lower()

        if not line:
            continue

        if tool == "ping" and "bytes from" in l:
            findings.append("Host is reachable via ICMP")

        elif tool == "nmap" and "/tcp" in l and "open" in l:
            findings.append(line)

        elif tool == "nikto" and line.startswith("+"):
            findings.append(line[1:].strip())

        elif tool == "whatweb" and "[" in line and "]" in line:
            findings.append(line)

        elif tool == "sslscan" and ("weak" in l or "deprecated" in l):
            findings.append(line)

    return findings


def parse_nuclei(items: List[dict]) -> List[str]:
    findings = []

    for item in items:
        name = item.get("info", {}).get("name")
        severity = item.get("info", {}).get("severity", "").upper()
        matched = item.get("matched-at")

        if name and matched:
            findings.append(f"[{severity}] {name} → {matched}")

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
    raw_findings["sslscan"] = parse_output("sslscan", run_sslscan(target))

    # ---- HTTPX JSON ----
    httpx_items = []
    for entry in run_httpx_json(target):
        tech = ", ".join(entry.get("tech", [])) or "Unknown"
        status = entry.get("status_code")
        if status:
            httpx_items.append(f"HTTP {status} | Technologies: {tech}")

    if httpx_items:
        raw_findings["httpx"] = httpx_items

    # ---- Nuclei JSON ----
    nuclei_items = parse_nuclei(run_nuclei_json(target))
    if nuclei_items:
        raw_findings["nuclei"] = nuclei_items

    # ---- Remove empty ----
    raw_findings = {k: v for k, v in raw_findings.items() if v}

    if not raw_findings:
        print("[!] No findings detected by tools")
        return state

    # ---- Enrich + terminal output ----
    enriched: Dict[str, List[dict]] = {}

    print("[+] Findings\n" + "-" * 60)

    for tool, items in raw_findings.items():
        enriched[tool] = []
        print(f"\n[{tool.upper()}]")

        for item in items:
            severity, score = assign_severity(item)
            confidence = calculate_confidence(tool, severity)

            enriched[tool].append({
                "data": item,
                "severity": severity,
                "cvss": score,
                "confidence": confidence
            })

            print(
                f" - {severity} ({score}) | "
                f"Confidence: {confidence} → {item}"
            )

    state.findings = enriched

    # ---- Normalize ----
    normalized = normalize_findings(enriched)

    # ---- AI / Offline summary (SAFE FALLBACK) ----
    try:
        roadmap = generate_remediation_roadmap(normalized)
    except Exception as e:
        print(f"[!] AI unavailable, using offline summary: {e}")
        roadmap = generate_offline_summary(normalized)

    # ---- JSON report ----
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    state.json_report = export_json_report(
        target, normalized, output_dir=REPORTS_DIR
    )
    print("\n[+] JSON report generated:", state.json_report)

    # ---- Skip reports if requested ----
    if "--no-report" in sys.argv:
        print("\n[!] --no-report enabled — skipping HTML/PDF generation")
        return state

    # ---- Risk heatmap ----
    state.heatmap = generate_risk_heatmap(
        enriched,
        output_dir=REPORTS_DIR
    )

    # ---- HTML report ----
    state.html_report = generate_html_report(
        target=target,
        tool_findings=enriched,
        normalized_findings=normalized,
        remediation_roadmap=roadmap,
        heatmap_path=state.heatmap,
        output_dir=REPORTS_DIR
    )

    # ---- PDF report ----
    if not is_termux():
        state.pdf_report = generate_pdf_report(state.html_report)
    else:
        print("[!] PDF skipped (Termux environment)")

    print("\n[+] HTML report generated:", state.html_report)
    if state.pdf_report:
        print("[+] PDF report generated:", state.pdf_report)

    return state

