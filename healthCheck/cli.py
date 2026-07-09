import socket
import sys
from pathlib import Path
from typing import Optional


import typer
from rich.console import Console
from rich.table import Table

from healthCheck.logger import setup_logger
from healthCheck.checks.cpu import check_cpu
from healthCheck.checks.memory import check_memory
from healthCheck.checks.disk import check_disk
from healthCheck.checks.uptime import check_uptime
from healthCheck.exporters.csv_exporter import export_csv
from healthCheck.exporters.json_exporter import export_json
from healthCheck.status import calculate_global_status, get_exit_code
from healthCheck.checks.ports import check_ports
from healthCheck.checks.services import check_services

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

@app.command()
def ports(
    port_list: str = typer.Option(
        ...,
        "--ports",
        "-p",
        help="Comma-separated list of ports to check. Example: 22,80,443,8081"
    ),
    host: str = typer.Option(
        "127.0.0.1",
        "--host",
        "-h",
        help="Host to check ports on"
    )
):
   
    logger.info("Starting port check for host: %s", host)

    try:
        parsed_ports = [
            int(port.strip())
            for port in port_list.split(",")
            if port.strip()
        ]
    except ValueError:
        logger.error("Invalid port list: %s", port_list)
        console.print("[red]Invalid port list. Use format like: 22,80,443,8081[/red]")
        sys.exit(3)

    report = check_ports(host, parsed_ports)

    logger.info("Port check completed with status: %s", report["status"])

    for check in report["checks"]:
        logger.info(
            "%s result: value=%s status=%s",
            check["name"],
            check["value"],
            check["status"]
        )

    print_table(report)

    sys.exit(get_exit_code(report["status"]))





@app.command()
def services(
    names: str = typer.Option(
        ...,
        "--names",
        "-n",
        help="Comma-separated list of services/processes to check. Example: chrome,python,docker"
    )
):
    """
    Check if specific services/processes are running.
    """

    logger.info("Starting service/process check")

    service_names = [
        name.strip()
        for name in names.split(",")
        if name.strip()
    ]

    if not service_names:
        logger.error("No service names provided")
        console.print("[red]No service names provided.[/red]")
        sys.exit(3)

    report = check_services(service_names)

    logger.info("Service/process check completed with status: %s", report["status"])

    for check in report["checks"]:
        logger.info(
            "%s result: value=%s status=%s",
            check["name"],
            check["value"],
            check["status"]
        )

    print_table(report)

    sys.exit(get_exit_code(report["status"]))


if __name__ == "__main__":
    app()