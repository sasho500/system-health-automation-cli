import sys

import typer
from rich.console import Console
from rich.table import Table

from healthCheck.checks.cpu import check_cpu
from healthCheck.checks.memory import check_memory
from healthCheck.checks.disk import check_disk
from healthCheck.checks.uptime import check_uptime


app = typer.Typer(help="System Health Automation CLI")
console = Console()


@app.callback()
def main():
 
    pass


def calculate_global_status(checks):
    statuses = [check["status"] for check in checks]

    if "CRITICAL" in statuses:
        return "CRITICAL"

    if "WARNING" in statuses:
        return "WARNING"

    return "OK"


def get_exit_code(status):
    if status == "OK":
        return 0

    if status == "WARNING":
        return 1

    if status == "CRITICAL":
        return 2

    return 3


@app.command()
def local():
 

    checks = [
        check_cpu(),
        check_memory(),
        check_disk(),
        check_uptime(),
    ]

    global_status = calculate_global_status(checks)

    table = Table(title="System Health Check")

    table.add_column("Check")
    table.add_column("Value")
    table.add_column("Status")
    table.add_column("Message")

    for check in checks:
        value = f"{check['value']}{check['unit']}"

        table.add_row(
            check["name"],
            str(value),
            check["status"],
            check["message"],
        )

    console.print(table)
    console.print(f"\nGlobal status: [bold]{global_status}[/bold]")

    sys.exit(get_exit_code(global_status))


if __name__ == "__main__":
    app()