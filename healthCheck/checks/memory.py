import psutil


def check_memory():
    memory = psutil.virtual_memory()
    usage = memory.percent
    if usage >= 90:
        status = "CRITICAL"
    elif usage >= 80:
        status = "WARNING"
    else:
        status = "OK"

    return {"name": "Memory", "value": usage, "status": status, "unit": "%", "message": f"Memory usage is at {usage}%."}

