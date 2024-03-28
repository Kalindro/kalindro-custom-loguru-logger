# logger_config.py

import os
import sys
import warnings

from loguru import logger

# Define default configuration
default_log_dir = None
default_level = 'INFO'
custom_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                 "<level>{level: <9}</level> | "
                 "<level>{message}</level> | "
                 "<blue>{function}</blue> | "
                 "<magenta>{file}:{line}</magenta>")


def setup_logging(log_dir=default_log_dir, level=default_level):
    """
    Reconfigure the loguru logger based on the given log directory and level.
    This function is intended to be used for optional reconfiguration.
    """
    logger.remove()  # Clear existing handlers

    if log_dir:
        if not os.path.exists(log_dir):
            warnings.warn(f"Provided log directory '{log_dir}' does not exist. Logging will proceed to stderr only.")
        else:
            logs_path = os.path.join(log_dir, "loguru_logs.log")
            logger.add(sink=logs_path, level="ERROR", format=custom_format)

    logger.add(sink=sys.stderr, level=level, format=custom_format)


# Automatically configure the logger with default settings on module import
setup_logging()

# Make the setup_logging function accessible via the logger object
logger.my_config = setup_logging
default_logger = logger
