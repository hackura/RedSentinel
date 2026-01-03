from typing import Dict, List
from redsentinel.core.external_tools import (
    run_nmap,
    run_nikto,
    run_nuclei,
)


def run_tools(target: str) -> Dict[str, List[dict]]:
    """
    Executes external security tools and returns
    raw findings compatible with the normalizer.
    """
    raw_findings: Dict[str, List[dict]] = {}

    raw_findings["nmap"] = run_nmap(target)
    raw_findings["nikto"] = run_nikto(target)
    raw_findings["nuclei"] = run_nuclei(target)

    return raw_findings

