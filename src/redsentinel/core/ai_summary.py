# ============================================================
# src/redsentinel/core/ai_summary.py
# ============================================================

from statistics import mean


def generate_offline_summary(normalized_findings: dict) -> str:
    """
    Heuristic AI-style summary (NO external AI required)
    """

    if not normalized_findings:
        return (
            "No security findings were identified during the scan. "
            "This suggests a low external exposure at the time of testing. "
            "Continuous monitoring is still recommended."
        )

    severity_counts = {
        "Critical": len(normalized_findings.get("Critical", [])),
        "High": len(normalized_findings.get("High", [])),
        "Medium": len(normalized_findings.get("Medium", [])),
        "Low": len(normalized_findings.get("Low", [])),
    }

    all_cvss = [
        f["cvss"]
        for findings in normalized_findings.values()
        for f in findings
        if f.get("cvss") is not None
    ]

    avg_cvss = round(mean(all_cvss), 2) if all_cvss else 0

    risk_level = (
        "CRITICAL" if severity_counts["Critical"] > 0 else
        "HIGH" if severity_counts["High"] > 0 else
        "MEDIUM" if severity_counts["Medium"] > 0 else
        "LOW"
    )

    summary = f"""
Security Summary (Offline Analysis)

The assessment identified a total of {sum(severity_counts.values())} findings.

Severity breakdown:
- Critical: {severity_counts["Critical"]}
- High: {severity_counts["High"]}
- Medium: {severity_counts["Medium"]}
- Low: {severity_counts["Low"]}

The average CVSS score across all findings is {avg_cvss}.

Overall Risk Assessment: {risk_level}

The results indicate potential weaknesses primarily related to service exposure,
configuration issues, or missing security controls. No exploitation was performed.

Recommended Actions:
- Address higher severity findings first
- Review exposed services and headers
- Apply secure configuration baselines
- Perform periodic reassessments
""".strip()

    return summary

