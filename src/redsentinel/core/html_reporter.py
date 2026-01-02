"""
RedSentinel HTML Reporter (FIXED TEMPLATE PATH)
---------------------------------------------
This version fixes the error:
  'report.html' not found in search path: 'templates'

It resolves the templates directory RELATIVE TO THE PACKAGE,
so it works when:
- running via venv
- running via pip install -e .
- running from anywhere
"""

import os
import re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

ANSI_ESCAPE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


def strip_ansi(text: str) -> str:
    if not text:
        return ""
    return ANSI_ESCAPE.sub("", text)


def normalize_findings(findings: dict) -> dict:
    normalized = {}
    for source, items in findings.items():
        clean_items = []
        for item in items:
            text = strip_ansi(str(item.get("data", item)))
            severity = item.get("severity", "MEDIUM")
            clean_items.append({
                "text": text,
                "severity": severity,
                "severity_class": f"severity-{severity.lower()}"
            })
        normalized[source] = clean_items
    return normalized


def generate_html_report(
    target: str,
    findings: dict,
    heatmap_path: str | None = None,
    output_dir: str = "reports",
) -> str:
    """Generate professional HTML report and return its path."""

    os.makedirs(output_dir, exist_ok=True)

    # ---------------- TEMPLATE PATH FIX ----------------
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.abspath(
        os.path.join(base_dir, "..", "..", "templates")
    )

    if not os.path.exists(os.path.join(templates_dir, "report.html")):
        raise FileNotFoundError(
            f"report.html not found in templates directory: {templates_dir}"
        )

    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html"]),
    )

    template = env.get_template("report.html")

    clean_findings = normalize_findings(findings)

    rendered = template.render(
        target=target,
        generated_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        findings=clean_findings,
        heatmap=heatmap_path,
    )

    filename = f"RedSentinel_Report_{target.replace('.', '_')}.html"
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    return output_path

