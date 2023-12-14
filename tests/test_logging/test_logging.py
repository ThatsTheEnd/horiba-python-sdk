import os

import pytest

from horiba_sdk import logging_config
from horiba_sdk.devices import DeviceManager


@pytest.mark.skip(reason='Does not work from general test suite. Only if executed locally in the file.')
def test_device_manager_logging():
    # Arrange
    log_file = os.path.abspath('test_log.log')  # use an absolute path
    logging_config.add_handler(log_file)
    expected_message = 'DeviceManager initialized.'

    # Act
    DeviceManager(start_icl=False)
    # Assert
    try:
        with open(log_file) as f:
            log_contents = f.read()
            assert expected_message in log_contents
    finally:
        # Clean up
        logging_config.remove_handler(1)
        if os.path.isfile(log_file):
            os.remove(log_file)
