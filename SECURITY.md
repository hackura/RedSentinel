# Security Policy

## Supported Versions

RedSentinel is currently in **Alpha**. Only the latest version in the `main` branch is supported.

Security fixes will be applied to:

* `main` branch
* Latest tagged release

Older commits are **not supported**.

---

## Reporting a Vulnerability

If you discover a security vulnerability **in RedSentinel itself** (not in scanned targets):

📧 **Email:** [hackura.security@proton.me](mailto:hackura.security@proton.me)
🔐 **PGP:** Available on request

Please include:

* A clear description of the issue
* Steps to reproduce
* Affected version or commit hash
* Potential impact

You will receive an acknowledgment within **72 hours**.

---

## Responsible Disclosure

We follow responsible disclosure practices:

* Do **not** publicly disclose vulnerabilities before a fix is released
* Allow reasonable time for remediation
* Coordinate on disclosure timelines if requested

---

## Scope

This policy applies to:

* RedSentinel source code
* CLI behavior
* Report generation logic
* AI prompt handling
* Dependency usage

This policy **does NOT** apply to:

* Targets scanned using RedSentinel
* Findings generated against third-party systems
* External tools (nmap, nikto, whatweb, etc.)

---

## Safe Usage Notice

RedSentinel performs **non-intrusive reconnaissance and analysis only**.

Users must:

* Own the target system, or
* Have explicit written authorization to test

Unauthorized use may violate local or international laws.

---

## Security Best Practices for Users

* Run RedSentinel inside a virtual environment
* Keep dependencies updated
* Never commit `.env` files
* Store reports securely
* Treat findings as sensitive data

---

## Acknowledgements

We appreciate responsible security researchers and contributors who help improve RedSentinel.

Thank you for helping keep the project secure.

