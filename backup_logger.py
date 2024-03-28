import os
import sys
import warnings

from loguru import logger


class CallableLogger:
    """A logger that is both callable for setting levels and used for logging, with optional logging directory.

    Parameters:
    - log_dir: Optional; the directory where logs should be saved. If the directory does not exist,
      a warning will be issued, and logging will only print to stderr.
    """

    LEVELS = {
        'INFO': 'INFO',
        'DEBUG': 'DEBUG',
        'ERROR': 'ERROR'
    }

    def __init__(self, log_dir=None):
        self.log_dir = log_dir
        self.custom_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                              "<level>{level: <9}</level> | "
                              "<level>{message}</level> | "
                              "<blue>{function}</blue> | "
                              "<magenta>{file}:{line}</magenta>")
        self.level = 'INFO'
        self._configure_logger(self.level)

    def __call__(self, level=None):
        if level:
            if level not in self.LEVELS.values():
                raise ValueError(f"Invalid logging level: {level}. Available levels are: {list(self.LEVELS.keys())}")
            self.level = level
            self._configure_logger(level)

    def _configure_logger(self, level):
        logger.remove()  # Remove any previously added handlers
        if self.log_dir and os.path.exists(self.log_dir):  # Check if log_dir exists
            logs_path = os.path.join(self.log_dir, "errors.log")
            logger.add(sink=logs_path, level=self.LEVELS['ERROR'], format=self.custom_format)
        elif self.log_dir:
            warnings.warn(f"Provided log directory '{self.log_dir}' does not exist. Logging will proceed to stderr only.")
        logger.add(sink=sys.stderr, level=level, format=self.custom_format)

    def __getattr__(self, name):
        """Delegate logging methods to the loguru logger, with a hint that a callable is returned."""
        return getattr(logger, name)


# Instantiate the callable logger
default_logger = CallableLogger()
