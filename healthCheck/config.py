from copy import deepcopy
from pathlib import Path

import yaml


DEFAULT_CONFIG = {
    "thresholds": {
        "cpu": {
            "warning": 80,
            "critical": 90,
        },
        "memory": {
            "warning": 80,
            "critical": 90,
        },
        "disk": {
            "warning": 85,
            "critical": 95,
        },
    }
}


def merge_configs(default_config, user_config):

    for key, value in user_config.items():
        if (
            key in default_config
            and isinstance(default_config[key], dict)
            and isinstance(value, dict)
        ):
            merge_configs(default_config[key], value)
        else:
            default_config[key] = value

    return default_config


def load_config(config_path=None):

    config = deepcopy(DEFAULT_CONFIG)

    if config_path is None:
        return config

    path = Path(config_path)

    if not path.exists():
        return config

    with path.open("r", encoding="utf-8") as file:
        user_config = yaml.safe_load(file) or {}

    return merge_configs(config, user_config)


def get_thresholds(config, check_name):
   

    thresholds = config["thresholds"][check_name]

    return thresholds["warning"], thresholds["critical"]