import psutil
from pathlib import Path


def check_disk():
    disk_path = Path.home().anchor or "/"
    disk = psutil.disk_usage(disk_path)
    usage = disk.percent

    if usage >= 95:
        status = "CRITICAL"
    elif usage >= 85:
        status = "WARNING"
    else:
        status = "OK"

    return {
        "name": "Disk",
        "value": usage,
        "unit": "%",
        "status": status,
        "message": f"Disk usage on {disk_path} is {usage}%"
    }
    


