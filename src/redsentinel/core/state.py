"""
Global session state for RedSentinel
"""

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

