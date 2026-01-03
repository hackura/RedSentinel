# ============================================================
# src/redsentinel/core/html_reporter.py
# ============================================================

from datetime import datetime
from statistics import mean
from pathlib import Path
from importlib.resources import files

from jinja2 import Environment, BaseLoader, select_autoescape


# =========================
# Executive Risk Score
# =========================

def calculate_executive_risk_score(findings: dict) -> float:
    scores = []

    for severity_group in findings.values():
        for f in severity_group:
            cvss = float(f.get("cvss", 0))
            confidence = float(f.get("confidence", 0.5))
            scores.append(cvss * confidence)

    if not scores:
        return 0.0

    return round(min(10.0, mean(scores)), 2)


# =========================
# Helpers
# =========================

def shorten(text: str, limit: int = 300) -> str:
    if not text:
        return ""
    return text if len(text) <= limit else text[:limit] + "..."


# =========================
# HTML Report Generator
# =========================

def generate_html_report(
    target: str,
    tool_findings: dict,
    normalized_findings: dict,
    remediation_roadmap: str,
    heatmap_path: str | None = None,
    output_dir: Path | str = "reports",
) -> str:

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"report_{target.replace('.', '_')}.html"
    report_file = output_dir / filename

    generated_on = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    executive_risk_score = calculate_executive_risk_score(normalized_findings)

    template_text = files("redsentinel").joinpath(
        "templates/report.html"
    ).read_text(encoding="utf-8")

    env = Environment(
        loader=BaseLoader(),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    env.filters["shorten"] = shorten

    template = env.from_string(template_text)

    html = template.render(
        target=target,
        generated_on=generated_on,
        executive_risk_score=executive_risk_score,
        normalized_findings=normalized_findings,
        tool_findings=tool_findings,
        remediation_roadmap=remediation_roadmap,
        heatmap_path=heatmap_path,
    )

    report_file.write_text(html, encoding="utf-8")
    return str(report_file)

