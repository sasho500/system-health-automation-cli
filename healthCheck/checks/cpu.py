import psutil
from healthCheck.status import get_status

def check_cpu():
    usage = psutil.cpu_percent(interval=1)
    
    status = get_status(
        value=usage,
        warning=80,
        critical=90
    )

    return {"name":"CPU","value": usage, "status": status, "unit": "%", "message": f"CPU usage is at {usage}%."}
