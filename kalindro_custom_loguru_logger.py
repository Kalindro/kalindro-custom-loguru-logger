import os
import sys
import warnings
from typing import Any

from loguru import logger

# Define default configuration
default_level = 'INFO'
custom_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                 "<level>{level: <9}</level> | "
                 "<level>{message}</level> | "
                 "<blue>{function}</blue> | "
                 "<magenta>{file}:{line}</magenta>")


class MyLogger:
    def __init__(self, logger):
        self._logger = logger
        # Default configuration applied upon initialization
        self.my_config()

    def my_config(self, log_dir: str = None, level: str = default_level, format: str = custom_format):
        """
        Custom configuration method for the logger. It can be called to reconfigure logging.
        Parameters:
            log_dir (str): Optional; the directory where logs should be saved.
            level (str): Logging level as a string. Defaults to 'INFO'.
            format (str): Log message format.
        """
        self._logger.remove()  # Clear existing handlers

        # Configure standard output
        self._logger.add(sys.stderr, format=format, level=level)

        # Configure file logging if a directory is specified
        if log_dir:
            if not os.path.exists(log_dir):
                warnings.warn(f"Log directory '{log_dir}' does not exist. Logging will proceed to stderr only.")
            else:
                file_path = os.path.join(log_dir, "loguru_logs.log")
                self._logger.add(file_path, format=format, level=level, rotation="10 MB")

    def __getattr__(self, item: str) -> Any:
        """
        Delegate attribute access to the underlying loguru logger instance.
        This allows the MyLogger instance to be used just like a loguru logger.
        """
        return getattr(self._logger, item)


# Instantiate MyLogger with the loguru logger
default_logger = MyLogger(logger)
