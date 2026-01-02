# ============================================================
# src/redsentinel/core/analyzer.py
# ============================================================
"""
Analyzer Module (Corrected)
--------------------------
This keeps YOUR original logic but adapts it to the new
RedSentinel pipeline:

- ❌ No global STATE
- ✅ Returns structured findings
- ✅ Exposes analyze_target() (required by simulator)
- ✅ Works for log / scan file analysis
"""

from typing import Dict, List
import os


# ------------------------------------------------------------
# Core analyzer entry point (REQUIRED by simulator)
# ------------------------------------------------------------

def analyze_target(target: str) -> Dict[str, List[str]]:
    """
    Entry point expected by simulator.

    If target is a file → analyze file contents
    If target is a hostname → simulate / placeholder (for now)
    """

    if os.path.isfile(target):
        return analyze_file(target)

    # --- Placeholder for live scanning (future) ---
    return {
        "web": [
            "Missing X-Frame-Options header",
            "Server banner disclosed",
        ]
    }


# ------------------------------------------------------------
# File-based analysis (YOUR ORIGINAL LOGIC, CLEANED)
# ------------------------------------------------------------

def analyze_file(filepath: str) -> Dict[str, List[str]]:
    print(f"\n[+] Analyzing file: {filepath}\n")

    findings = set()

    try:
        with open(filepath, "r", errors="ignore") as f:
            for line in f:
                l = line.lower()

                # ---------------- AUTH LOG SIGNALS ----------------
                if "failed password" in l:
                    findings.add("Failed authentication attempts detected")

                if "invalid user" in l:
                    findings.add("Invalid user login attempts detected")

                if "authentication failure" in l:
                    findings.add("Authentication failure events detected")

                # ---------------- WEB / HEADER SIGNALS ----------------
                if "x-frame-options" in l and "not present" in l:
                    findings.add("Missing X-Frame-Options header")

                if "x-content-type-options" in l and "not set" in l:
                    findings.add("Missing X-Content-Type-Options header")

                if "content-security-policy" in l and "not present" in l:
                    findings.add("Missing Content-Security-Policy header")

                if "x-powered-by" in l:
                    findings.add("X-Powered-By header disclosed")

                if "server:" in l:
                    findings.add("Server banner disclosed")

                # ---------------- REDIRECTS ----------------
                if "uncommon header" in l and "refresh" in l:
                    findings.add("Client-side redirect via Refresh header")

    except Exception as e:
        print(f"[!] Error reading file: {e}")
        return {}

    if not findings:
        print("[+] No significant findings detected")
        return {}

    print("[+] Findings identified:")
    for f in sorted(findings):
        print(f" - {f}")

    # Structured return (required by simulator)
    return {
        "logs": sorted(findings)
    }

