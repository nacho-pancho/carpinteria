import logging

from logging import DEBUG
from logging import WARNING
from logging import INFO

def get_logger():
    if get_logger._logger is None:
        logging.basicConfig(level=logging.INFO)
        get_logger._logger = logging.getLogger()
    return get_logger._logger
get_logger._logger = None

def set_logging_level(level):
    get_logger().setLevel(level)

def debug_mode():
    return get_logger().level == logging.DEBUG
