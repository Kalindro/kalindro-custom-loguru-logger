import os
import sys
import typing as tp
import warnings
from typing import Literal

from loguru._logger import Core as _Core, Logger as _Logger

# Custom logging format, it's pretty
_CUSTOM_FORMAT = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                  "<level>{level: <9}</level> | "
                  "<level>{message}</level> | "
                  "<blue>{function}</blue> | "
                  "<magenta>{file}:{line}</magenta>")

# Available logging levels
_LogLevelsType = Literal["DEBUG", "INFO", "ERROR"]
_VALID_LEVELS = list(tp.get_args(_LogLevelsType))


class ConfiguredLoguru(_Logger):
    """
    My configured Loguru Logger. It inherits the Loguru logger the same way the actual Loguru does in the main import. Defaults to "INFO" level
    in console, no dumping directory. Available log levels described in "_LogLevelsType".
    """

    def __init__(self):
        core = _Core()
        super().__init__(core=core, exception=None, depth=0, record=False, lazy=False, colors=False, raw=False, capture=True, patchers=[], extra={})
        self.initialize_logger()

    def initialize_logger(self):
        """Executed on class init that's done on import, removes all the default handlers and sets the console level to "INFO"."""
        self.remove()
        self.set_console_level("INFO")

    def set_console_level(self, level: _LogLevelsType):
        """Set console prints level to the desired one. Also removes other console handlers."""
        if level not in _VALID_LEVELS:
            raise ValueError(f"Invalid logging level: {level}. Available levels are: {_VALID_LEVELS}")

        with self._core.lock:
            handlers = self._core.handlers.copy()
        for handler_id, handler in handlers.items():
            if "stderr" in str(handler._name):
                self.remove(handler_id)

        self.add(sink=sys.stderr, level=level.upper(), format=_CUSTOM_FORMAT)

    def set_logs_dump_location(self, log_dir, level: _LogLevelsType = "ERROR"):
        """Set logs directory location to dump. Also removes directory dump handlers."""
        if level not in _VALID_LEVELS:
            raise ValueError(f"Invalid logging level: {level}. Available levels are: {_VALID_LEVELS}")
        if not os.path.exists(log_dir):
            warnings.warn(f"Provided log directory '{log_dir}' does not exist. Creating now")
            os.mkdir(log_dir)

        with self._core.lock:
            handlers = self._core.handlers.copy()
        for handler_id, handler in handlers.items():
            if "stderr" not in str(handler._name):
                self.remove(handler_id)

        logs_path = os.path.join(log_dir, "loguru_logs.log")
        if os.path.exists(logs_path):
            os.remove(logs_path)

        self.add(sink=logs_path, level=level, format=_CUSTOM_FORMAT)


# Make the class initialize on startup
default_logger = ConfiguredLoguru()
