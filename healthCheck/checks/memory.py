import psutil

from healthCheck.status import get_status


def check_memory(warning=80, critical=90):
    memory = psutil.virtual_memory()
    usage = memory.percent

    status = get_status(
        value=usage,
        warning=warning,
        critical=critical,
    )

    return {
        "name": "Memory",
        "value": usage,
        "unit": "%",
        "status": status,
        "message": f"Memory usage is {usage}%",
    }