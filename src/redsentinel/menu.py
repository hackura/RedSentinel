#!/usr/bin/env python3
"""
RedSentinel - Interactive CLI Menu
AI-Assisted SOC Simulation Framework (Educational)
"""

import time
import sys

from redsentinel.core.analyzer import analyze_file
from redsentinel.core.planner import generate_plan
from redsentinel.core.simulator import simulate_scan


BANNER = r"""
██████╗ ███████╗██████╗ ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗
██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║
██████╔╝█████╗  ██║  ██║███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║
██╔══██╗██╔══╝  ██║  ██║╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║
██║  ██║███████╗██████╔╝███████║███████╗██   ████║   ██║   ██║██║ ╚████║███████╗███████╗
╚═╝  ╚═╝╚══════╝╚═════╝ ╚══════╝╚══════╝╚════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚═
"""

SUBTITLE = "AI-Assisted SOC Simulation Framework"


def pause():
    input("\n[Press ENTER to continue]")


def print_menu():
    print("\nSelect an action:\n")
    print("  1. Analyze Scan / Log File")
    print("  2. Generate Attack Plan")
    print("  3. Simulate Vulnerability Scan")
    print("  4. Exit")


def launch_menu():
    while True:
        print("\033c", end="")  # clear screen
        print(BANNER)
        print(SUBTITLE)
        print("-" * 60)

        print_menu()
        choice = input("\nRedSentinel > ").strip()

        # EXIT
        if choice == "4":
            print("\n[+] Exiting RedSentinel. Stay sharp ")
            sys.exit(0)

        
        # ANALYZE
        elif choice == "1":
            file_path = input("\nEnter scan/log file path: ").strip()
            print("\n[+] Processing input...")
            time.sleep(1)
            try:
                analyze_file(file_path)
            except Exception as e:
                print(f"[!] Analysis failed: {e}")
            pause()

        # PLAN
        elif choice == "2":
            target = input("\nEnter target: ").strip()
            print("\n[+] Generating AI-assisted attack plan...")
            time.sleep(1)
            try:
                generate_plan(target, framework="mitre")
            except Exception as e:
                print(f"[!] Planning failed: {e}")
            pause()

        # SIMULATE
        elif choice == "3":
            target = input("\nEnter target: ").strip()
            print(f"\n[+] Simulating reconnaissance and vulnerability discovery for: {target}")
            print("[*] AI agent is analyzing the attack surface...\n")
            try:
                simulate_scan(target)
            except KeyboardInterrupt:
                print("\n[!] Simulation interrupted by user.")
            except Exception as e:
                print(f"[!] Simulation failed: {e}")
            pause()

        else:
            print("\n[!] Invalid option.")
            pause()

