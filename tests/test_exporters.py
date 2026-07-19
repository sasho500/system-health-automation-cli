import json
import csv

from healthCheck.exporters.json_exporter import export_json
from healthCheck.exporters.csv_exporter import export_csv


def test_export_json_creates_file(tmp_path):
    report = {
        "host": "localhost",
        "status": "OK",
        "checks": [
            {
                "name": "CPU",
                "value": 10,
                "unit": "%",
                "status": "OK",
                "message": "CPU usage is 10%",
            }
        ],
    }

    output_file = tmp_path / "health.json"

    export_json(report, output_file)

    assert output_file.exists()

    with output_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["host"] == "localhost"
    assert data["status"] == "OK"


def test_export_csv_creates_file(tmp_path):
    report = {
        "host": "localhost",
        "status": "OK",
        "checks": [
            {
                "name": "CPU",
                "value": 10,
                "unit": "%",
                "status": "OK",
                "message": "CPU usage is 10%",
            }
        ],
    }

    output_file = tmp_path / "health.csv"

    export_csv(report, output_file)

    assert output_file.exists()

    with output_file.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert rows[0]["host"] == "localhost"
    assert rows[0]["check"] == "CPU"
    assert rows[0]["status"] == "OK"