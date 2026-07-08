def get_status(value, warning, critical):

    if value >= critical:
        return "CRITICAL"

    if value >= warning:
        return "WARNING"

    return "OK"


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