import os

from kalindro_custom_loguru_logger import default_logger as logger

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
LOG_DIR = os.path.join(PROJECT_DIR, "_logs/")

logger.set_console_level("INFO")
logger.set_console_level("INFO")
logger.set_logs_dump_location(LOG_DIR)
logger.set_logs_dump_location(LOG_DIR)

with logger._core.lock:
    handlers = logger._core.handlers.copy()
for handler_id, handler in handlers.items():
    print(handler)

logger.debug("This is debug")
logger.info("This is info")
logger.warning("This is warning")
logger.error("This is error")


def number():
    return 5 / 0


try:
    x = number() + 8
except Exception as err:
    logger.bind(no_console_traceback=True).exception(f"This is exception with bind: {err}")
    logger.exception(f"This is exception without bind: {err}")
