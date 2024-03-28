from loguru import logger
import os
import sys
import warnings


class ExtendedLogger:
    def __init__(self):
        self._logger = logger
        self.default_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                               "<level>{level: <8}</level> | "
                               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                               "<level>{message}</level>")
        # Initialize with default configuration
        self.setup_logging()

    def setup_logging(self, log_dir=None, level='INFO'):
        """
        A method to configure logging. This can be called to reconfigure logging.
        """
        self._logger.remove()  # Clear existing handlers

        # Configure standard output
        self._logger.add(sys.stderr, format=self.default_format, level=level)

        # Configure file logging if a directory is specified
        if log_dir:
            if not os.path.exists(log_dir):
                warnings.warn(f"Log directory '{log_dir}' does not exist. Logging will proceed to stderr only.")
            else:
                file_path = os.path.join(log_dir, "loguru_logs.log")
                self._logger.add(file_path, format=self.default_format, level=level, rotation="10 MB")

    def __getattr__(self, item):
        """
        Forward attribute access to the underlying loguru logger instance.
        """
        return getattr(self._logger, item)

default_logger = ExtendedLogger()