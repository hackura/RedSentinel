# ============================================================
# src/redsentinel/core/risk_heatmap.py
# ============================================================

from pathlib import Path
import matplotlib.pyplot as plt


def generate_risk_heatmap(findings: dict, output_dir: Path) -> str:
    """
    Generates a risk heatmap based on enriched findings.

    - Saves into src/redsentinel/reports
    - Returns filename only (HTML/PDF safe)
    """

    severity_count = {
        "Critical": 0,
        "High": 0,
        "Medium": 0,
        "Low": 0,
    }

    # Count findings by severity
    for tool_findings in findings.values():
        for f in tool_findings:
            sev = f.get("severity", "").capitalize()
            if sev in severity_count:
                severity_count[sev] += 1

    labels = list(severity_count.keys())
    values = list(severity_count.values())
    colors = ["darkred", "red", "orange", "green"]

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=colors)
    plt.title("Risk Severity Distribution")
    plt.xlabel("Severity")
    plt.ylabel("Number of Findings")

    for i, v in enumerate(values):
        plt.text(i, v + 0.05, str(v), ha="center", fontsize=9)

    output_dir.mkdir(parents=True, exist_ok=True)
    heatmap_file = output_dir / "risk_heatmap.png"

    plt.tight_layout()
    plt.savefig(heatmap_file, dpi=150)
    plt.close()

    # 🔑 RETURN ONLY FILENAME
    return heatmap_file.name

