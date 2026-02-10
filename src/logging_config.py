"""
Central logging configuration for the trading bot.

All modules should import and use `get_logger(__name__)`.
Logs are written to `bot.log` in the project root with timestamps
and basic contextual information.
"""

import logging
import logging.handlers
import os
from typing import Optional


LOG_FILE_NAME = "bot.log"


def setup_logging(log_level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """
    Configure root logger with a rotating file handler and console handler.
    Safe to call multiple times; subsequent calls are no-ops.
    """
    if logging.getLogger().handlers:
        # Already configured
        return

    log_path = log_file or LOG_FILE_NAME
    log_dir = os.path.dirname(os.path.abspath(log_path)) or "."
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    setup_logging()
    return logging.getLogger(name)



