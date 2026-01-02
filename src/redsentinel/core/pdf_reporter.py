import subprocess
import os

def generate_pdf_report(html_path: str) -> str:
    if not html_path or not html_path.endswith(".html"):
        raise ValueError("Invalid HTML path for PDF generation")

    pdf_path = html_path.replace(".html", ".pdf")

    try:
        subprocess.run(
            ["wkhtmltopdf", html_path, pdf_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        print(f"[+] PDF report generated: {pdf_path}")
        return pdf_path

    except Exception as e:
        print(f"[!] PDF generation failed: {e}")
        return None

