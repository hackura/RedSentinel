import sys
from pathlib import Path
import argparse
import json

# =========================
# Load environment variables EARLY
# =========================
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=Path(".env"))
except ImportError:
    pass

from redsentinel.menu import launch_menu
from redsentinel.doctor import run_doctor
from redsentinel.core.simulator import simulate_scan
from redsentinel.core.planner import (
    generate_attack_plan,
    generate_remediation_plan
)
from redsentinel.core.utils import load_latest_report
from redsentinel.core.state import REPORTS_DIR

VERSION = "0.1.0"
AUTHOR = "Hackura"
GITHUB = "https://github.com/hackura/redsentinel"


def ensure_venv():
    if sys.prefix == sys.base_prefix:
        print("RedSentinel must be run inside a virtual environment.")
        sys.exit(1)


# =========================
# About
# =========================

def show_about():
    print(f"""
RedSentinel
-----------
AI-Assisted Security Assessment Tool

Author: {AUTHOR}
Version: {VERSION}
License: MIT

GitHub: {GITHUB}
""")


# =========================
# Scan log reader
# =========================

def show_scan_log(filepath: str):
    path = Path(filepath)

    if not path.exists():
        print(f"[!] Scan log not found: {filepath}")
        return

    print("\n[+] Scan Log Viewer\n" + "-" * 50)
    print("File:", path.name)

    if path.suffix == ".json":
        data = json.loads(path.read_text())
        print("Target:", data.get("target", "Unknown"))

        for tool, items in data.get("findings", {}).items():
            print(f"\n[{tool.upper()}]")
            for item in items:
                print(
                    f" - {item.get('severity')} "
                    f"({item.get('cvss')}) | "
                    f"{item.get('data')}"
                )
        return

    if path.suffix == ".log":
        print(path.read_text())
        return

    print("[!] Unsupported scan log format")


# =========================
# CLI
# =========================

def main():
    parser = argparse.ArgumentParser(
        prog="redsentinel",
        description="RedSentinel – AI-Assisted Security Assessment Tool"
    )

    parser.add_argument("--about", action="store_true", help="Show tool information")
    parser.add_argument("--scan-log", metavar="FILE", help="Read an existing scan log")

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("doctor", help="Check environment & dependencies")

    scan = subparsers.add_parser("scan", help="Run live security scan")
    scan.add_argument("target", help="Target domain or IP")

    plan = subparsers.add_parser("plan", help="Generate plan")
    plan.add_argument("target", help="Target domain or IP")
    plan.add_argument(
        "--remediate",
        action="store_true",
        help="Generate remediation plan from latest scan"
    )

    subparsers.add_parser("logs", help="List stored scan reports")

    args = parser.parse_args()

    # ---------- GLOBAL FLAGS ----------
    if args.about:
        show_about()
        return

    if args.scan_log:
        ensure_venv()
        show_scan_log(args.scan_log)
        return

    # ---------- COMMANDS ----------
    if args.command == "doctor":
        ensure_venv()
        run_doctor()
        return

    if args.command == "scan":
        ensure_venv()
        simulate_scan(args.target)
        return

    if args.command == "plan":
        ensure_venv()

        # ---- REMEDIATION PLAN ----
        if args.remediate:
            report = load_latest_report(args.target)
            if not report:
                print("[!] No scan report found. Run `redsentinel scan <target>` first.")
                return

            steps = generate_remediation_plan(report)

            print("\n[+] Remediation Plan\n" + "-" * 40)
            for step in steps:
                print(
                    f"- [{step['severity']}] {step['issue']}\n"
                    f"  → {step['recommendation']}"
                )
            return

        # ---- ATTACK PLAN ----
        generate_attack_plan(args.target)
        return

    if args.command == "logs":
        ensure_venv()

        files = list(REPORTS_DIR.glob("*.json")) + list(REPORTS_DIR.glob("*.log"))
        if not files:
            print("[!] No scan logs found")
            return

        print("\n[+] Available scan logs:\n")
        for f in sorted(files):
            print(" -", f.name)
        return

    # ---------- DEFAULT ----------
    ensure_venv()
    launch_menu()


if __name__ == "__main__":
    main()

