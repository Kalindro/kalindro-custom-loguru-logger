import os
import sys
import warnings

from loguru import logger

# Define the default log directory path
DEFAULT_LOG_DIR = "_logs"


class CallableLogger:
    """A logger that is both callable for setting levels and used for logging."""

    LEVELS = {
        'INFO': 'INFO',
        'DEBUG': 'DEBUG',
        'ERROR': 'ERROR'
    }

    def __init__(self):
        self.custom_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                              "<level>{level: <9}</level> | "
                              "<level>{message}</level> | "
                              "<blue>{function}</blue> | "
                              "<magenta>{file}:{line}</magenta>")
        self.level = 'INFO'
        self._configure_logger(self.level)

    def __call__(self, level=None):
        """Allow the logger's level to be set by calling the instance."""
        if level:
            if level not in self.LEVELS.values():
                raise ValueError(f"Invalid logging level: {level}. Available levels are: {list(self.LEVELS.keys())}")
            self.level = level
            self._configure_logger(level)

    def _configure_logger(self, level):
        """Configure the underlying loguru logger."""
        logger.remove()
        self._ensure_log_directory()
        logs_path = os.path.join(DEFAULT_LOG_DIR, "errors.log")
        logger.add(sink=logs_path, level=self.LEVELS['ERROR'], format=self.custom_format)
        logger.add(sink=sys.stderr, level=level, format=self.custom_format)

    @staticmethod
    def _ensure_log_directory():
        """Ensure that the log directory exists."""
        if not os.path.exists(DEFAULT_LOG_DIR):
            warnings.warn(f"Folder '{DEFAULT_LOG_DIR}' was not found in main directory. Please create it manually.")

    def __getattr__(self, name):
        """Delegate logging methods to the loguru logger."""
        return getattr(logger, name)


# Instantiate the callable logger
default_logger = CallableLogger()
