import sys

from loguru import logger


def set_level(level: str) -> None:
    """
    Sets the logging level for the library.

    Args:
        level (str): The logging level. Should be one of :
        'TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'.
    """
    logger.add(sys.stderr, level=level.upper())


def add_handler(path: str, level: str = 'INFO') -> None:
    """
    Adds a new handler to the logger.

    Args:
        path (str): The path to the log file.
        level (str, optional): The logging level. Defaults to 'INFO'.
    """
    logger.add(path, level=level.upper())


def remove_handler(index: int) -> None:
    """
    Removes a handler from the logger.

    Args:
        index (int): The index of the handler to remove.
    """
    logger.remove(index)
