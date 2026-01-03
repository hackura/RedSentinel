import sys
from pathlib import Path

# =========================
# Load environment variables EARLY (Python 3.13 safe)
# =========================
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=Path(".env"))
except ImportError:
    print("[!] python-dotenv not installed. Skipping .env loading.")

from redsentinel.menu import launch_menu


def ensure_venv():
    if sys.prefix == sys.base_prefix:
        print("  RedSentinel must be run inside a virtual environment.")
        print("  python -m venv venv && source venv/bin/activate")
        sys.exit(1)


def main():
    ensure_venv()
    launch_menu()


if __name__ == "__main__":
    main()

