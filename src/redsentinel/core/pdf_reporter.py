# ============================================================
# src/redsentinel/core/pdf_reporter.py
# ============================================================

from pathlib import Path

try:
    from weasyprint import HTML
except ImportError:
    HTML = None


def generate_pdf_report(html_report_path: str) -> str | None:
    """
    Convert HTML report to PDF using WeasyPrint.
    """

    if HTML is None:
        print("[!] WeasyPrint not installed — skipping PDF generation")
        return None

    html_file = Path(html_report_path)
    if not html_file.exists():
        print("[!] HTML report not found")
        return None

    pdf_file = html_file.with_suffix(".pdf")

    try:
        HTML(
            filename=str(html_file),
            base_url=str(html_file.parent.resolve())
        ).write_pdf(
            str(pdf_file),
            presentational_hints=True
        )
    except Exception as e:
        print(f"[!] PDF generation failed: {e}")
        return None

    return str(pdf_file)

