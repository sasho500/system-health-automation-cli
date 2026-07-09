import socket

from healthCheck.status import calculate_global_status


def check_single_port(host, port, timeout=2):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))

            if result == 0:
                status = "OK"
                state = "OPEN"
                message = f"Port {port} is open on {host}"
            else:
                status = "CRITICAL"
                state = "CLOSED"
                message = f"Port {port} is closed on {host}"

            return {
                "name": f"Port {port}",
                "value": state,
                "unit": "",
                "status": status,
                "message": message,
            }

    except Exception as error:
        return {
            "name": f"Port {port}",
            "value": "UNKNOWN",
            "unit": "",
            "status": "UNKNOWN",
            "message": f"Failed to check port {port} on {host}: {error}",
        }


def check_ports(host, ports):
    checks = []

    for port in ports:
        checks.append(check_single_port(host, port))

    global_status = calculate_global_status(checks)

    return {
        "host": host,
        "status": global_status,
        "checks": checks,
    }