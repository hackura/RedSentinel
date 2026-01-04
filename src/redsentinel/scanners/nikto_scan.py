import subprocess
from redsentinel.utils.tools import tool_status


def run_nikto(target):
    tools = tool_status()

    if not tools["nikto"]:
        return {
            "tool": "nikto",
            "status": "skipped",
            "reason": "nikto not installed",
            "output": ""
        }

    if not tools["perl"]:
        return {
            "tool": "nikto",
            "status": "skipped",
            "reason": "perl not installed (required for nikto)",
            "output": ""
        }

    try:
        result = subprocess.run(
            ["nikto", "-h", target],
            capture_output=True,
            text=True,
            timeout=180
        )

        return {
            "tool": "nikto",
            "status": "success",
            "reason": None,
            "output": result.stdout
        }

    except Exception as e:
        return {
            "tool": "nikto",
            "status": "failed",
            "reason": str(e),
            "output": ""
        }

