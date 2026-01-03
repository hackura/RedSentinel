from redsentinel.core.ai_client import AIClient


def generate_remediation_roadmap(normalized_findings: dict) -> str:
    if not normalized_findings:
        return (
            "No high-confidence security findings were identified during "
            "this assessment. Maintain standard security hygiene and "
            "continue regular monitoring."
        )

    try:
        client = AIClient()

        prompt = (
            "You are a senior security consultant.\n\n"
            "Based on the following normalized security findings, "
            "produce a clear remediation roadmap prioritised by risk.\n\n"
            f"{normalized_findings}"
        )

        response = client.generate(
            system_prompt="You are a cybersecurity expert.",
            user_prompt=prompt
        )

        return response.strip()

    except Exception as e:
        # HARD fallback (never fails)
        return (
            "Automated remediation guidance could not be generated at this time.\n\n"
            "Recommended next steps:\n"
            "- Review all Medium and High severity findings\n"
            "- Apply vendor security best practices\n"
            "- Restrict unnecessary network exposure\n"
            "- Implement security headers and TLS hardening\n"
            "- Schedule follow-up assessments\n\n"
            f"AI Error: {str(e)}"
        )

