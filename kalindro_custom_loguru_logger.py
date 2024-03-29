import os
import sys
import warnings

from loguru import logger

default_level = 'INFO'
custom_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                 "<level>{level: <9}</level> | "
                 "<level>{message}</level> | "
                 "<blue>{function}</blue> | "
                 "<magenta>{file}:{line}</magenta>")

LEVELS = {
    'INFO': 'INFO',
    'DEBUG': 'DEBUG',
    'ERROR': 'ERROR'
}


def my_config(level=default_level, log_dir=None):
    """
    Reconfigure the loguru logger based on the given log directory and level.
    This function is intended to be used for optional reconfiguration.
    """

    logger.remove()  # Clear existing handlers
    if level:
        if level not in LEVELS.values():
            raise ValueError(f"Invalid logging level: {level}. Available levels are: {list(LEVELS.keys())}")
        logger.add(sink=sys.stderr, level=level, format=custom_format)

    if log_dir:
        if not os.path.exists(log_dir):
            warnings.warn(f"Provided log directory '{log_dir}' does not exist. Logging will proceed to stderr only.")
        else:
            logs_path = os.path.join(log_dir, "loguru_logs.log")
            logger.add(sink=logs_path, level="ERROR", format=custom_format)


my_config()

logger.my_config = my_config
default_logger = logger
