# ============================================================
# src/redsentinel/core/html_reporter.py
# ============================================================

from datetime import datetime
from statistics import mean
from pathlib import Path
from importlib.resources import files

from jinja2 import Environment, BaseLoader, select_autoescape


# =========================
# Executive Risk Scoring
# =========================

def calculate_executive_risk_score(findings: dict) -> float:
    """
    Produces a single executive-friendly risk score (0–10)
    based on CVSS scores and confidence.
    """
    scores = []

    for tool_findings in findings.values():
        for f in tool_findings:
            cvss = f.get("cvss", 0)
            confidence = f.get("confidence", 0.5)
            scores.append(cvss * confidence)

    if not scores:
        return 0.0

    return round(min(10.0, mean(scores)), 2)


# =========================
# HTML Report Generator
# =========================

def generate_html_report(
    target: str,
    results: dict,
    findings: dict,
    remediation_roadmap: str,
    heatmap_path: str | None = None,
    output_dir: str = "reports",
) -> str:
    """
    Generates an HTML security report using a packaged Jinja2 template.
    Fully compatible with pip installs.
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = f"report_{target.replace('.', '_')}.html"
    report_file = output_path / filename

    generated_on = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    executive_risk_score = calculate_executive_risk_score(findings)

    # --------------------------------------------------
    # Load packaged template (SAFE AFTER INSTALL)
    # --------------------------------------------------

    template_text = files("redsentinel").joinpath(
        "templates/report.html"
    ).read_text(encoding="utf-8")

    env = Environment(
        loader=BaseLoader(),
        autoescape=select_autoescape(["html", "xml"])
    )

    template = env.from_string(template_text)

    # --------------------------------------------------
    # Render HTML
    # --------------------------------------------------

    html = template.render(
        target=target,
        generated_on=generated_on,
        executive_risk_score=executive_risk_score,
        heatmap_path=heatmap_path,
        results=results,
        remediation_roadmap=remediation_roadmap,
    )

    report_file.write_text(html, encoding="utf-8")
    return str(report_file)

