import os
import sys
import warnings

from loguru import logger


class LoggerWrapper:
    def __init__(self):
        self._logger = logger
        self.default_log_dir = None
        self.default_level = 'INFO'
        self.custom_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                              "<level>{level: <9}</level> | "
                              "<level>{message}</level> | "
                              "<blue>{function}</blue> | "
                              "<magenta>{file}:{line}</magenta>")
        self.setup_logging()

    def setup_logging(self, log_dir=None, level='INFO'):
        self._logger.remove()  # Clear existing handlers
        if log_dir:
            if not os.path.exists(log_dir):
                warnings.warn(f"Log directory '{log_dir}' does not exist. Logging will proceed to stderr only.")
            else:
                logs_path = os.path.join(log_dir, "loguru_logs.log")
                self._logger.add(sink=logs_path, level="ERROR", format=self.custom_format)
        self._logger.add(sink=sys.stderr, level=level, format=self.custom_format)

    def __getattr__(self, item):
        return getattr(self._logger, item)


# Use the wrapper
default_logger = LoggerWrapper()
