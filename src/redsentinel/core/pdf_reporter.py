# ============================================================
# src/redsentinel/core/pdf_reporter.py
# ============================================================

from pathlib import Path
from weasyprint import HTML


def generate_pdf_report(html_path: str) -> str | None:
    """
    Generates a PDF from an HTML report using WeasyPrint.
    Fully compatible with packaged assets.
    """

    html_file = Path(html_path)

    if not html_file.exists():
        print("[!] HTML report not found, skipping PDF generation")
        return None

    pdf_file = html_file.with_suffix(".pdf")

    try:
        # base_url is CRITICAL for images & assets
        HTML(
            filename=str(html_file),
            base_url=str(html_file.parent.resolve())
        ).write_pdf(str(pdf_file))

        print(f"[+] PDF report generated: {pdf_file}")
        return str(pdf_file)

    except Exception as e:
        print(f"[!] PDF generation failed: {e}")
        return None

