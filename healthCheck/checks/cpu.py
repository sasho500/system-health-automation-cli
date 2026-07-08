import psutil

def check_cpu():
    usage = psutil.cpu_percent(interval=1)
    
    if usage >= 90:
        status = "CRITICAL"
    elif usage >= 80:
        status = "WARNING"
    else:
        status = "OK"

    return {"name":"CPU","value": usage, "status": status, "unit": "%", "message": f"CPU usage is at {usage}%."}
