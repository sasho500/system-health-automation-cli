import psutil

from healthCheck.status import calculate_global_status


def normalize_process_name(name):
    return name.lower().replace(".exe", "").strip()


def check_single_service(service_name):
    target_name = normalize_process_name(service_name)

    for process in psutil.process_iter(["name"]):
        try:
            process_name = process.info.get("name")

            if not process_name:
                continue

            normalized_name = normalize_process_name(process_name)

            if normalized_name == target_name:
                return {
                    "name": service_name,
                    "value": "RUNNING",
                    "unit": "",
                    "status": "OK",
                    "message": f"{service_name} is running",
                }

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return {
        "name": service_name,
        "value": "STOPPED",
        "unit": "",
        "status": "CRITICAL",
        "message": f"{service_name} is not running",
    }


def check_services(service_names):
    checks = []

    for service_name in service_names:
        checks.append(check_single_service(service_name))

    global_status = calculate_global_status(checks)

    return {
        "host": "localhost",
        "status": global_status,
        "checks": checks,
    }