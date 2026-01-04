import subprocess
from redsentinel.utils.tools import tool_status


def run_nmap(target):
    tools = tool_status()

    if not tools["nmap"]:
        return {
            "tool": "nmap",
            "status": "skipped",
            "reason": "nmap not installed",
            "output": ""
        }

    try:
        result = subprocess.run(
            ["nmap", "-Pn", target],
            capture_output=True,
            text=True,
            timeout=120
        )

        return {
            "tool": "nmap",
            "status": "success",
            "reason": None,
            "output": result.stdout
        }

    except subprocess.TimeoutExpired:
        return {
            "tool": "nmap",
            "status": "failed",
            "reason": "scan timed out",
            "output": ""
        }

    except Exception as e:
        return {
            "tool": "nmap",
            "status": "failed",
            "reason": str(e),
            "output": ""
        }

