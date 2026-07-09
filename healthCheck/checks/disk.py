import psutil
from pathlib import Path

from healthCheck.status import get_status


def check_disk(warning=85, critical=95):
    disk_path = Path.home().anchor or "/"
    disk = psutil.disk_usage(disk_path)
    usage = disk.percent

    status = get_status(
        value=usage,
        warning=warning,
        critical=critical,
    )

    return {
        "name": "Disk",
        "value": usage,
        "unit": "%",
        "status": status,
        "message": f"Disk usage on {disk_path} is {usage}%",
    }