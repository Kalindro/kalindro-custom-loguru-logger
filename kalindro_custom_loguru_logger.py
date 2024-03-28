from loguru import logger
import os
import sys
import warnings


class MyLogger:
    def __init__(self):
        self._logger = logger
        self.default_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                               "<level>{level: <8}</level> | "
                               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                               "<level>{message}</level>")
        # Automatically configure with default settings
        self.setup_logging()

    def setup_logging(self, log_dir=None, level='INFO'):
        """
        Configures the underlying loguru logger instance with the specified log directory and level.
        This method can be called multiple times to reconfigure the logger.
        """
        # Remove all handlers
        self._logger.remove()

        # Set format and level for stderr
        self._logger.add(sys.stderr, format=self.default_format, level=level)

        # Configure file logging if a directory is provided
        if log_dir is not None:
            if not os.path.exists(log_dir):
                warnings.warn(f"Log directory '{log_dir}' does not exist. Logging will proceed to stderr only.")
            else:
                log_file_path = os.path.join(log_dir, "app.log")
                self._logger.add(log_file_path, format=self.default_format, level=level, rotation="10 MB")

    def __getattr__(self, name):
        """
        Delegate attribute access to the underlying loguru logger instance.
        This allows the MyLogger instance to be used just like a loguru logger.
        """
        return getattr(self._logger, name)

default_logger = MyLogger()