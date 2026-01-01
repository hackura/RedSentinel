#!/usr/bin/env python3

import argparse
import os

def init_project(name: str):
    """
    Initialize a new RedSentinel project workspace.
    """
    folders = ["inputs", "outputs", "reports"]

    print(f"[+] Initializing RedSentinel project: {name}")

    for folder in folders:
        path = os.path.join(name, folder)
        os.makedirs(path, exist_ok=True)
        print(f"    └── created {path}")

    print("[+] Project initialized successfully.")


def main():
    parser = argparse.ArgumentParser(
        prog="redsentinel",
        description="RedSentinel - AI-assisted red team CLI (authorized use only)"
    )

    subparsers = parser.add_subparsers(dest="command")

    # init command
    init_parser = subparsers.add_parser(
        "init",
        help="Initialize a new RedSentinel project"
    )
    init_parser.add_argument(
        "--name",
        required=True,
        help="Name of the project directory"
    )

    args = parser.parse_args()

    if args.command == "init":
        init_project(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
