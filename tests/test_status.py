from healthCheck.status import get_status, calculate_global_status, get_exit_code


def test_get_status_ok():
    assert get_status(value=50, warning=80, critical=90) == "OK"


def test_get_status_warning():
    assert get_status(value=85, warning=80, critical=90) == "WARNING"


def test_get_status_critical():
    assert get_status(value=95, warning=80, critical=90) == "CRITICAL"


def test_calculate_global_status_ok():
    checks = [
        {"status": "OK"},
        {"status": "OK"},
    ]

    assert calculate_global_status(checks) == "OK"


def test_calculate_global_status_warning():
    checks = [
        {"status": "OK"},
        {"status": "WARNING"},
    ]

    assert calculate_global_status(checks) == "WARNING"


def test_calculate_global_status_critical():
    checks = [
        {"status": "OK"},
        {"status": "CRITICAL"},
    ]

    assert calculate_global_status(checks) == "CRITICAL"


def test_calculate_global_status_unknown():
    checks = [
        {"status": "OK"},
        {"status": "UNKNOWN"},
    ]

    assert calculate_global_status(checks) == "UNKNOWN"


def test_get_exit_code():
    assert get_exit_code("OK") == 0
    assert get_exit_code("WARNING") == 1
    assert get_exit_code("CRITICAL") == 2
    assert get_exit_code("UNKNOWN") == 3