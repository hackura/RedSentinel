# src/redsentinel/doctor.py

import sys
import os
import shutil
import platform
from rich.console import Console
from rich.table import Table

console = Console()


# -----------------------------
# Helpers
# -----------------------------

def which(cmd):
    return shutil.which(cmd)


def has_python_version():
    return sys.version_info >= (3, 10)


def is_termux():
    return "TERMUX_VERSION" in os.environ or os.path.exists("/data/data/com.termux")


def detect_os():
    if is_termux():
        return "Termux (Android)"
    return platform.system()


def check_optional(pkg):
    try:
        __import__(pkg)
        return True
    except ImportError:
        return False


# -----------------------------
# Checks
# -----------------------------

def run_doctor():
    console.rule("[bold red]RedSentinel Doctor")

    os_name = detect_os()

    # Python checks
    python_ok = has_python_version()
    console.print(
        f"[{'green' if python_ok else 'red'}]{'✓' if python_ok else '✗'} Python {platform.python_version()}[/]"
    )

    # Core tools
    tools = {
        "nmap": which("nmap"),
        "nikto": which("nikto") or which("nikto.pl"),
        "whatweb": which("whatweb"),
        "perl": which("perl"),
        "ruby": which("ruby"),
    }

    table = Table(title="System Dependencies")
    table.add_column("Component")
    table.add_column("Status")
    table.add_column("Details")

    for name, path in tools.items():
        if path:
            table.add_row(name, "[green]✓ Found[/green]", path)
        else:
            table.add_row(name, "[red]✗ Missing[/red]", "-")

    console.print(table)

    # Optional features
    console.rule("[bold]Optional Features")

    visuals = check_optional("matplotlib") and check_optional("numpy")
    reports = check_optional("weasyprint")

    console.print(
        f"[{'green' if visuals else 'yellow'}]{'✓' if visuals else '!'} Visual charts (matplotlib/numpy)[/]"
    )
    console.print(
        f"[{'green' if reports else 'yellow'}]{'✓' if reports else '!'} PDF reports (weasyprint)[/]"
    )

    # Suggestions
    console.rule("[bold]Suggested Actions")

    if not python_ok:
        console.print("[red]• Upgrade Python to >= 3.10[/red]")

    if not tools["nmap"]:
        console.print("[yellow]• Install nmap[/yellow]")

    if not tools["nikto"]:
        console.print("[yellow]• Install Nikto (requires Perl)[/yellow]")

    if not tools["whatweb"]:
        console.print("[yellow]• Install WhatWeb (requires Ruby)[/yellow]")

    if tools["nikto"] and not tools["perl"]:
        console.print("[red]• Perl is required for Nikto[/red]")

    if tools["whatweb"] and not tools["ruby"]:
        console.print("[red]• Ruby is required for WhatWeb[/red]")

    if not visuals:
        console.print("[blue]• pip install redsentinel[visuals][/blue]")

    if not reports:
        console.print("[blue]• pip install redsentinel[reports][/blue]")

    console.print("\n[bold green]Doctor check completed.[/bold green]")

