import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "healthcheck.log"

    logger = logging.getLogger("healthcheck")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger