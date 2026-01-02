"""
Pentest report generator
"""

from datetime import datetime
from redsentinel.core.state import STATE


def generate_report():
    if not STATE["target"]:
        print("[!] No target set. Cannot generate report.")
        return

    report = []
    report.append("# RedSentinel Pentest Report\n")
    report.append(f"**Target:** {STATE['target']}\n")
    report.append(f"**Date:** {datetime.utcnow()} UTC\n")

    report.append("\n## Findings\n")
    for f in STATE["findings"]:
        report.append(f"- {f}")

    report.append("\n## Vulnerabilities & Risk\n")
    for name, data in STATE["risk"].items():
        report.append(f"- **{name}**: {data['severity']} (Score: {data['score']})")

    report.append("\n## Conclusion\n")
    report.append(
        "The identified issues indicate potential security weaknesses that "
        "should be addressed based on risk priority."
    )

    final_report = "\n".join(report)
    STATE["report"] = final_report

    with open("report.md", "w") as f:
        f.write(final_report)

    print("[+] Pentest report generated.")
    print("[+] Saved as report.md\n")
    print("----- REPORT SUMMARY -----")
    print(final_report)

