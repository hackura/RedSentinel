"""
utils.py
--------
Helper utilities for loading reports and shared logic.
"""

import json
from pathlib import Path
from redsentinel.core.state import REPORTS_DIR


def load_latest_report(target: str) -> dict | None:
    """
    Load the most recent scan report for a given target.
    """
    if not REPORTS_DIR.exists():
        return None

    candidates = sorted(
        REPORTS_DIR.glob(f"*{target}*.json"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )

    if not candidates:
        return None

    try:
        return json.loads(candidates[0].read_text())
    except Exception:
        return None

