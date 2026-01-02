import sys
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

