import psutil

from healthCheck.status import get_status


def check_cpu(warning=80, critical=90):
    usage = psutil.cpu_percent(interval=1)

    status = get_status(
        value=usage,
        warning=warning,
        critical=critical,
    )

    return {
        "name": "CPU",
        "value": usage,
        "unit": "%",
        "status": status,
        "message": f"CPU usage is {usage}%",
    }