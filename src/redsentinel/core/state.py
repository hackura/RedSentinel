from pathlib import Path

# ============================================================
# Global paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = BASE_DIR / "reports"


STATE = {
    "target": None,
    "findings": [],
    "vulnerabilities": [],
    "risk": {},
    "report": ""
}


def reset():
    STATE["target"] = None
    STATE["findings"].clear()
    STATE["vulnerabilities"].clear()
    STATE["risk"].clear()
    STATE["report"] = ""

