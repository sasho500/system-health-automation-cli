import csv
from pathlib import Path


def export_csv(report, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    checks = report["checks"]

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["host", "check", "value", "unit", "status", "message"]
        )

        writer.writeheader()

        for check in checks:
            writer.writerow({
                "host": report["host"],
                "check": check["name"],
                "value": check["value"],
                "unit": check["unit"],
                "status": check["status"],
                "message": check["message"]
            })

    return path