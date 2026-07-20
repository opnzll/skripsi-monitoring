"""
Application logging configuration.

This module configures logging for the entire
Smart Energy Monitoring application.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ==========================================================
# CONSTANTS
# ==========================================================

LOG_DIRECTORY = Path("logs")

SYSTEM_LOG = LOG_DIRECTORY / "system.log"

ERROR_LOG = LOG_DIRECTORY / "error.log"

LOG_LEVEL = logging.INFO

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

BACKUP_COUNT = 5

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ==========================================================
# CONFIGURE LOGGING
# ==========================================================

def configure_logging() -> None:
    """
    Configure application logging.

    Creates:

    logs/
        system.log
        error.log
    """

    LOG_DIRECTORY.mkdir(
        exist_ok=True,
    )

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    root_logger.setLevel(LOG_LEVEL)

    # ------------------------------------------------------
    # SYSTEM LOG
    # ------------------------------------------------------

    system_handler = RotatingFileHandler(
        SYSTEM_LOG,
        maxBytes=MAX_FILE_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )

    system_handler.setLevel(logging.INFO)

    system_handler.setFormatter(
        formatter,
    )

    # ------------------------------------------------------
    # ERROR LOG
    # ------------------------------------------------------

    error_handler = RotatingFileHandler(
        ERROR_LOG,
        maxBytes=MAX_FILE_SIZE,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )

    error_handler.setLevel(logging.ERROR)

    error_handler.setFormatter(
        formatter,
    )

    # ------------------------------------------------------
    # CONSOLE
    # ------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)

    console_handler.setFormatter(
        formatter,
    )

    # ------------------------------------------------------
    # REGISTER
    # ------------------------------------------------------

    root_logger.addHandler(
        system_handler,
    )

    root_logger.addHandler(
        error_handler,
    )

    root_logger.addHandler(
        console_handler,
    )

    root_logger.info(
        "Logging initialized successfully."
    )