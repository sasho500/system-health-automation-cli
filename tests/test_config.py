from healthCheck.config import load_config, get_thresholds


def test_load_default_config_when_file_missing():
    config = load_config("missing-config.yaml")

    cpu_warning, cpu_critical = get_thresholds(config, "cpu")

    assert cpu_warning == 80
    assert cpu_critical == 90


def test_get_disk_thresholds_from_default_config():
    config = load_config("missing-config.yaml")

    disk_warning, disk_critical = get_thresholds(config, "disk")

    assert disk_warning == 85
    assert disk_critical == 95