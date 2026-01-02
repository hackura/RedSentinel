from redsentinel.analyzer import analyze_findings

def test_analyze_findings_assigns_severity():
    dummy_findings = [
        {"name": "Missing Security Headers"},
        {"name": "Information Disclosure"}
    ]

    analyzed = analyze_findings(dummy_findings)

    assert len(analyzed) == 2
    for item in analyzed:
        assert "severity" in item
