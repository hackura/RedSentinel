import os
import matplotlib.pyplot as plt


def generate_risk_heatmap(findings: list, output_dir: str):
    """
    Generate a simple risk heatmap from raw string findings
    """

    severity_count = {
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for f in findings:
        if not isinstance(f, str):
            continue

        text = f.lower()

        if "missing" in text or "disclosure" in text:
            severity_count["Medium"] += 1
        elif "open port" in text:
            severity_count["Low"] += 1
        else:
            severity_count["Low"] += 1

    labels = list(severity_count.keys())
    values = list(severity_count.values())

    plt.figure()
    plt.bar(labels, values)
    plt.title("Risk Heatmap")
    plt.xlabel("Severity")
    plt.ylabel("Count")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "risk_heatmap.png")

    plt.savefig(output_path)
    plt.close()

    return output_path

