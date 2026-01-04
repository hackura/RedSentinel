import subprocess
from redsentinel.utils.tools import tool_status


def run_whatweb(target):
    tools = tool_status()

    if not tools["whatweb"]:
        return {
            "tool": "whatweb",
            "status": "skipped",
            "reason": "whatweb not installed",
            "output": ""
        }

    if not tools["ruby"]:
        return {
            "tool": "whatweb",
            "status": "skipped",
            "reason": "ruby not installed (required for whatweb)",
            "output": ""
        }

    try:
        result = subprocess.run(
            ["whatweb", target],
            capture_output=True,
            text=True,
            timeout=120
        )

        return {
            "tool": "whatweb",
            "status": "success",
            "reason": None,
            "output": result.stdout
        }

    except Exception as e:
        return {
            "tool": "whatweb",
            "status": "failed",
            "reason": str(e),
            "output": ""
        }

