import socket
import sys
from pathlib import Path
from typing import Optional

from healthCheck.logger import setup_logger

import typer
from rich.console import Console
from rich.table import Table

from healthCheck.checks.cpu import check_cpu
from healthCheck.checks.memory import check_memory
from healthCheck.checks.disk import check_disk
from healthCheck.checks.uptime import check_uptime
from healthCheck.exporters.csv_exporter import export_csv
from healthCheck.exporters.json_exporter import export_json
from healthCheck.status import calculate_global_status, get_exit_code


app = typer.Typer(help="System Health Automation CLI")
console = Console()
logger = setup_logger()

@app.callback()
def main():
  
    pass


def build_report():
    checks = [
        check_cpu(),
        check_memory(),
        check_disk(),
        check_uptime(),
    ]

    global_status = calculate_global_status(checks)

    return {
        "host": socket.gethostname(),
        "status": global_status,
        "checks": checks
    }


def print_table(report):
    table = Table(title="System Health Check")

    table.add_column("Check")
    table.add_column("Value")
    table.add_column("Status")
    table.add_column("Message")

    for check in report["checks"]:
        value = f"{check['value']}{check['unit']}"

        table.add_row(
            check["name"],
            str(value),
            check["status"],
            check["message"],
        )

    console.print(table)
    console.print(f"\nGlobal status: [bold]{report['status']}[/bold]")


@app.command()
def local(
    output_format: str = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output format: table, json, csv"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path for json/csv export"
    )
):
    
    
    """
    Run local system health check.
    """
    logger.info("Starting local system health check")
    
    report = build_report()
    
    logger.info("Health check completed with status: %s", report["status"])
    
    
    for check in report["checks"]:
        logger.info(
            "%s check result: value=%s%s status=%s",
            check["name"],
            check["value"],
            check["unit"],
            check["status"]
        )
    
    if output_format == "table":
        print_table(report)

    elif output_format == "json":
        if output is None:
            output = Path("reports/health.json")

        export_json(report, output)
        console.print(f"JSON report exported to: [bold]{output}[/bold]")

    elif output_format == "csv":
        if output is None:
            output = Path("reports/health.csv")

        export_csv(report, output)
        console.print(f"CSV report exported to: [bold]{output}[/bold]")

    else:
        console.print(f"[red]Unsupported format:[/red] {output_format}")
        sys.exit(3)

    sys.exit(get_exit_code(report["status"]))


if __name__ == "__main__":
    app()