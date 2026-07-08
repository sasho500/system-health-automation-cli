import psutil
from datetime import datetime

def check_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    uptime = now - boot_time
    uptime_value = str(uptime).split(".")[0]

    return {
        "name": "Uptime",
        "value": uptime_value,
        "unit": "",
        "status": "OK",
        "message": f"System uptime is {uptime_value}"
    }