import psutil
from healthCheck.status import get_status


def check_memory():
    memory = psutil.virtual_memory()
    usage = memory.percent
    
    status = get_status(
        value=usage,
        warning=80,
        critical=90
    )

    return {"name": "Memory", "value": usage, "status": status, "unit": "%", "message": f"Memory usage is at {usage}%."}

