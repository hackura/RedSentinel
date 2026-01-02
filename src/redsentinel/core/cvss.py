# ============================================================
# src/redsentinel/core/cvss.py
# ============================================================
"""
CVSS v3.1 Scoring Module (Your Implementation, Integrated)
---------------------------------------------------------
This keeps YOUR CVSS math exactly as-is and simply adds
an adapter function `assign_severity()` so the rest of
RedSentinel can consume it cleanly.

Public API exposed:
- calculate_cvss_base(vector)
- severity_from_score(score)
- assign_severity(finding)
"""

import math

# ---------------- CVSS v3.1 WEIGHTS ----------------

AV = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2}
AC = {"L": 0.77, "H": 0.44}
PR_U = {"N": 0.85, "L": 0.62, "H": 0.27}   # Scope Unchanged
PR_C = {"N": 0.85, "L": 0.68, "H": 0.50}   # Scope Changed
UI = {"N": 0.85, "R": 0.62}
IMPACT = {"N": 0.0, "L": 0.22, "H": 0.56}


# ---------------- CVSS BASE SCORE ----------------

def calculate_cvss_base(vector: dict) -> float:
    """
    Calculate CVSS v3.1 Base Score
    """

    iss = 1 - (
        (1 - IMPACT[vector["C"]]) *
        (1 - IMPACT[vector["I"]]) *
        (1 - IMPACT[vector["A"]])
    )

    if vector["S"] == "U":
        impact = 6.42 * iss
        pr = PR_U[vector["PR"]]
    else:
        impact = 7.52 * (iss - 0.029) - 3.25 * pow((iss - 0.02), 15)
        pr = PR_C[vector["PR"]]

    exploitability = 8.22 * (
        AV[vector["AV"]] *
        AC[vector["AC"]] *
        pr *
        UI[vector["UI"]]
    )

    if impact <= 0:
        score = 0.0
    else:
        if vector["S"] == "U":
            score = min(impact + exploitability, 10)
        else:
            score = min(1.08 * (impact + exploitability), 10)

    return round_up(score)


def round_up(score: float) -> float:
    return math.ceil(score * 10) / 10


def severity_from_score(score: float) -> str:
    if score >= 9.0:
        return "CRITICAL"
    elif score >= 7.0:
        return "HIGH"
    elif score >= 4.0:
        return "MEDIUM"
    elif score > 0:
        return "LOW"
    return "NONE"


# ------------------------------------------------------------
# Adapter REQUIRED by simulator.py
# ------------------------------------------------------------

def assign_severity(finding):
    """
    Adapter for simulator.

    Since we don't yet extract full CVSS vectors from tools,
    we use SAFE DEFAULTS and let your real CVSS math handle scoring.

    Later: map findings → real vectors.
    """

    # Temporary default vector (network, low complexity)
    vector = {
        "AV": "N",
        "AC": "L",
        "PR": "N",
        "UI": "N",
        "S": "U",
        "C": "L",
        "I": "L",
        "A": "N",
    }

    score = calculate_cvss_base(vector)
    severity = severity_from_score(score)

    return severity, score

