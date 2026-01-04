# RedSentinel

<p align="center">
  <img src="assets/redsentinel-logo.png" width="160" alt="RedSentinel Logo" />
</p>

<p align="center">
<strong>AI-Assisted Security Assessment & Planning Framework</strong><br>
Educational • Research • Defensive & Blue-Team Focused
</p>

<p align="center">
  <a href="https://pypi.org/project/redsentinel/">
    <img src="https://img.shields.io/pypi/v/redsentinel.svg" alt="PyPI version">
  </a>
  <a href="https://pypi.org/project/redsentinel/">
    <img src="https://img.shields.io/pypi/dm/redsentinel.svg" alt="PyPI downloads">
  </a>
  <a href="https://pypi.org/project/redsentinel/">
    <img src="https://img.shields.io/pypi/pyversions/redsentinel.svg" alt="Python versions">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/pypi/l/redsentinel.svg" alt="License">
  </a>
</p>

<p align="center">
<a href="https://pypi.org/project/redsentinel/">PyPI</a> •
<a href="https://github.com/hackura/redsentinel">GitHub</a>
</p>

---

## Overview

**RedSentinel** is an AI-assisted security assessment framework that supports **live defensive scanning**, **attack planning**, **log analysis**, and **remediation planning** — all from a single, unified CLI.

It orchestrates industry-standard tools, normalizes their output, enriches findings with risk context, and generates **professional-grade insights** usable by:

* Blue teams
* Security students
* Researchers
* SOC analysts

🚫 **No exploitation. No payloads. No intrusion.**
RedSentinel is designed for **authorized, defensive security testing only**.

---

## What Makes RedSentinel Different

✔ Dual-mode operation: **interactive menu + full CLI**
✔ Works **online or fully offline**
✔ Supports **external scan logs** (`.json`, `.log`)
✔ Termux-aware & low-resource friendly
✔ Designed as a **learning + professional tool**

---

## Tool Coverage

![nmap](https://img.shields.io/badge/nmap-active-blue)
![nikto](https://img.shields.io/badge/nikto-active-blue)
![whatweb](https://img.shields.io/badge/whatweb-active-blue)
![sslscan](https://img.shields.io/badge/sslscan-active-blue)
![ping](https://img.shields.io/badge/ping-active-blue)

Unavailable tools are **automatically skipped** — no crashes.

---

## CLI Usage

### Show help

```bash
redsentinel --help
```

### About the tool

```bash
redsentinel --about
```

### Environment & dependency check

```bash
redsentinel doctor
```

---

## Scanning

### Run a live defensive scan

```bash
redsentinel scan example.com
```

* Executes available tools only
* Generates structured scan artifacts
* Safe defaults (no exploitation)

<p align="center">
  <img src="assets/cli.png" width="90%" alt="CLI output" />
</p>

---

## Planning

### Generate an **Attack / Engagement Plan** (NO scanning)

```bash
redsentinel plan example.com
```

Produces a **red-team style attack plan**, including:

* Recon steps
* Attack surface mapping
* Credential & access checks
* MITRE-aligned methodology

✔ Offline
✔ No tools required

---

### Generate a **Remediation Plan** (Post-scan)

```bash
redsentinel plan example.com --remediate
```

* Loads the **latest scan report**
* Generates prioritized remediation steps
* No live scanning required

---

## Logs & Analysis

### List available scan artifacts

```bash
redsentinel logs
```

### View a scan log

```bash
redsentinel --scan-log reports/example.com.json
redsentinel --scan-log /var/log/nmap_scan.log
```

✔ External directories supported
✔ Read-only & safe

---

## Interactive Menu

```bash
redsentinel
```

<p align="center">
  <img src="assets/cli_in_action.png" width="90%" alt="Menu in action" />
</p>

---

## Demo

<p align="center">
  <img src="assets/redsentinel-demo.gif" width="90%" alt="RedSentinel demo" />
</p>

---

## Installation (PyPI – Recommended)

```bash
pip install redsentinel
```

---

## Manual Installation (Dev)

```bash
git clone https://github.com/hackura/RedSentinel.git
cd RedSentinel

python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## Termux (Android)

```bash
pkg update && pkg upgrade
pkg install python git clang openssl libxml2 libxslt perl ruby
pkg install nmap sslscan

git clone https://github.com/sullo/nikto.git
git clone https://github.com/urbanadventurer/WhatWeb.git

pip install redsentinel
```

---

## AI-Assisted Intelligence

RedSentinel includes **offline-safe AI logic** and optional online AI enrichment to:

* Summarize scan results
* Explain risks in plain language
* Generate remediation guidance

✔ Offline fallback supported

---

## 🛣️ Roadmap

### v0.1.x (Current)

* ✔ Interactive menu + full CLI
* ✔ Defensive scanning (nmap, nikto, whatweb)
* ✔ Attack planning (offline)
* ✔ Remediation planning (post-scan)
* ✔ External log analysis
* ✔ Termux support

### v0.2.x (Next)

* ⏳ AI-powered scan summarization (online + offline)
* ⏳ JSON / PDF export for plans
* ⏳ Framework selector (`--framework mitre|owasp`)
* ⏳ Improved report templates

### v0.3.x

* ⏳ CI/CD friendly non-interactive mode
* ⏳ Plugin system for tools
* ⏳ Risk scoring improvements

### v1.0 (Long-Term)

* ⏳ Stable API
* ⏳ Enterprise-ready reporting
* ⏳ Educational lab mode
* ⏳ Community plugins

---

## Disclaimer

RedSentinel is intended for **authorized defensive security testing only**.
You must own the target or have permission before scanning.

---

**RedSentinel — Hackura Project**
Educational & Research Use Only

