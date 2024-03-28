import os
import sys
import warnings

from loguru import logger


def configure_logger(log_dir=None, level='INFO'):
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

    if level not in LEVELS.values():
        raise ValueError(f"Invalid logging level: {level}. Available levels are: {list(LEVELS.keys())}")

    logger.remove()  # Remove any previously added handlers
    if log_dir and os.path.exists(log_dir):  # Check if log_dir exists
        logs_path = os.path.join(log_dir, "errors.log")
        logger.add(sink=logs_path, level=LEVELS['ERROR'], format=custom_format)
    elif log_dir:
        warnings.warn(f"Provided log directory '{log_dir}' does not exist. Logging will proceed to stderr only.")
    logger.add(sink=sys.stderr, level=level, format=custom_format)


# Dynamically add the configure method to the logger
logger.configure = configure_logger
default_logger = logger
