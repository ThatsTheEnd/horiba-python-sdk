from loguru import logger

from horiba_sdk import logging_config


def test_set_level():
    # Arrange
    level = 'DEBUG'

    # Act
    logging_config.set_level(level)

    # Assert
    assert logger._core.handlers, 'No handlers were set'
    # assert logger._core.handlers[0].level == logger.level(level).no, 'Incorrect level was set'
    # assert logger._core.handlers[0]._sink == sys.stderr, 'Incorrect sink was set'
