import os
import sys
import warnings
from typing import Any

from loguru import logger

_default_level = 'INFO'
_custom_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                  "<level>{level: <9}</level> | "
                  "<level>{message}</level> | "
                  "<blue>{function}</blue> | "
                  "<magenta>{file}:{line}</magenta>")

_LEVELS = {
    'INFO': 'INFO',
    'DEBUG': 'DEBUG',
    'ERROR': 'ERROR'
}


class ConfiguredLoguru(logger):
    def __init__(self):
        self.my_config()

    @staticmethod
    def my_config(level=_default_level, log_dir=None):
        """
        Reconfigure the loguru logger based on the given log directory and level.
        This function is intended to be used for optional reconfiguration.
        """

        logger.remove()  # Clear existing handlers
        if level:
            if level not in _LEVELS.values():
                raise ValueError(f"Invalid logging level: {level}. Available levels are: {list(_LEVELS.keys())}")
            logger.add(sink=sys.stderr, level=level, format=_custom_format)

        if log_dir:
            if not os.path.exists(log_dir):
                warnings.warn(f"Provided log directory '{log_dir}' does not exist. Logging will proceed to stderr only.")
            else:
                logs_path = os.path.join(log_dir, "loguru_logs.log")
                logger.add(sink=logs_path, level="ERROR", format=_custom_format)

    def __getattr__(self, item: str) -> Any:
        """
        Delegate attribute access to the underlying loguru logger instance.
        This allows the MyLogger instance to be used just like a loguru logger.
        """
        return getattr(self._logger, item)


default_logger = ConfiguredLoguru()
