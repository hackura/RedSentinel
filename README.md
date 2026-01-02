# 🛡️ RedSentinel

**RedSentinel** is an AI-assisted red team simulation and vulnerability assessment framework designed for **educational, research, and defensive security use**. It orchestrates real-world security tools to perform live scans, analyze findings, calculate CVSS severity, and generate **professional SOC-ready HTML and PDF reports**.

> ⚠️ **Authorization Required**: Only scan systems you own or have explicit permission to test.

---

## ✨ Key Features

* 🔍 **Live Vulnerability Scanning** (no fake data)
* 🧠 **AI-Assisted Analysis & Attack Planning**
* 📊 **Risk Heatmap Visualization**
* 📄 **Automatic HTML & PDF Report Generation**
* 🧮 **CVSS v3.1 Scoring & Severity Mapping**
* 🧪 **Menu-driven CLI Interface**

---

## 🧰 Tools Orchestrated (Mandatory for Live Scans)

RedSentinel does **NOT** re-implement scanners. Instead, it orchestrates industry-standard tools.

You **must install the following system tools** to enable live scanning:

| Tool      | Purpose                                        |
| --------- | ---------------------------------------------- |
| `nmap`    | Network & port discovery                       |
| `nikto`   | Web server vulnerability scanning              |
| `whatweb` | Web technology fingerprinting                  |
| `ping`    | Host availability check (usually preinstalled) |

### 📦 Install Tools (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install nmap nikto
sudo gem install whatweb
```

Verify installation:

```bash
nmap --version
nikto -Version
whatweb example.com
```

> If a tool is missing, RedSentinel will **warn and skip that scan** — it will never fabricate results.

---

## 🐍 Python Environment (MANDATORY)

RedSentinel **must be run inside a virtual environment**.

```bash
python3 -m venv venv
source venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## 📦 Installation (Editable / Development Mode)

```bash
pip install -e .
```

This installs the `redsentinel` CLI command.

---

## 🚀 Usage

Launch RedSentinel:

```bash
redsentinel
```

### Available Modes (Menu-Driven)

* 🔍 **Live Vulnerability Scan**
* 🧠 **Attack Planning / Advisory Mode**
* 📂 **Offline Log Analysis** (e.g. Nikto logs)

> **Important**: When a vulnerability scan is executed, **PDF generation is mandatory**.

---

## 📄 Reports

Every vulnerability scan produces:

* ✔️ Clean **HTML report**
* ✔️ High-quality **PDF report** (via WeasyPrint)
* ✔️ Embedded **risk heatmap**
* ✔️ Executive summary & findings table

Reports are saved to:

```
reports/
```

---

## 📊 CVSS & Severity

RedSentinel uses a **CVSS v3.1 scoring engine** to assign severity levels:

| Score Range | Severity |
| ----------- | -------- |
| 9.0 – 10.0  | CRITICAL |
| 7.0 – 8.9   | HIGH     |
| 4.0 – 6.9   | MEDIUM   |
| 0.1 – 3.9   | LOW      |

---

## 🧪 Project Structure (src-layout)

```
src/redsentinel
├── cli.py
├── menu.py
├── core
│   ├── analyzer.py
│   ├── simulator.py
│   ├── planner.py
│   ├── advisor.py
│   ├── cvss.py
│   ├── html_reporter.py
│   ├── pdf_reporter.py
│   ├── risk_heatmap.py
│   └── state.py
├── templates
│   └── report.html
└── assets
    └── risk_heatmap.png
```

---

## 🧪 Testing

```bash
pytest
```

Tests improve credibility and reliability.

---

## 🧠 Philosophy

* ❌ No fake vulnerabilities
* ❌ No silent failures
* ✅ Real tools, real findings
* ✅ SOC / client-ready reporting

---

## 📜 License

MIT License

---

## 🔮 Roadmap (Planned)

* MITRE ATT&CK mapping
* Scan profiles (fast / full / stealth)
* JSON export for SIEM
* Dockerized deployment
* BlueSentinel (defensive SOC mode)

---

## 👨‍💻 Author

**Hackura**
Cybersecurity Student & Researcher

---

> 🛑 **Reminder**: RedSentinel is for **authorized testing only**. Unauthorized scanning is illegal.

