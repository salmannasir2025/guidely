import logging
import sys

from pythonjsonlogger import jsonlogger


def setup_logging():
    """
    Configures structured JSON logging for the application.
    This is ideal for production environments and log analysis tools.
    """
    logger = logging.getLogger()
    # Prevent duplicate handlers if this is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s"
    )
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)
