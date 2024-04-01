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
    def __init__(self):
        core = _Core()
        super().__init__(core=core, exception=None, depth=0, record=False, lazy=False, colors=False, raw=False, capture=True, patchers=[], extra={})
        self.initialize_logger()

    def initialize_logger(self):
        self.remove()
        self.set_level(_default_level)

    def set_level(self, level):
        if level not in _LEVELS:
            raise ValueError(f"Invalid logging level: {level}. Available levels are: {list(_LEVELS.keys())}")

        with self._core.lock:
            handlers = self._core.handlers.copy()
        for handler_id, handler in handlers.items():
            if "stderr" in str(handler._name):
                self.remove(handler_id)

        self.add(sink=sys.stderr, level=level.upper(), format=_custom_format)

    def set_logs_dump_location(self, log_dir):
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

        self.add(sink=logs_path, level='ERROR', format=_custom_format)


default_logger = ConfiguredLoguru()
