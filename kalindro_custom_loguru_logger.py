import os
import sys
import warnings

from loguru._logger import Core as _Core, Logger as _Logger

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


class ConfiguredLoguru(_Logger):
    def __init__(self, level=_default_level, log_dir=None):
        core = _Core()
        super().__init__(core=core, exception=None, depth=0, record=False, lazy=False, colors=False, raw=False, capture=True, patchers=[], extra={})
        self.my_config(level, log_dir)

    def my_config(self, level=_default_level, log_dir=None):
        """
        Reconfigure the logger based on the given log directory and level.
        """
        self.remove()  # Clear existing handlers
        if level not in _LEVELS:
            raise ValueError(f"Invalid logging level: {level}. Available levels are: {list(_LEVELS.keys())}")
        self.add(sink=sys.stderr, level=level, format=_custom_format)

        if log_dir:
            if not os.path.exists(log_dir):
                warnings.warn(f"Provided log directory '{log_dir}' does not exist. Logging will proceed to stderr only.")
            else:
                logs_path = os.path.join(log_dir, "loguru_logs.log")
                self.add(sink=logs_path, level="ERROR", format=_custom_format)


# Usage
default_logger = ConfiguredLoguru()
