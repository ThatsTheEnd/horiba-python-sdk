# pylint: skip-file

import pytest
import os
from horiba_sdk.communication import TelnetCommunicator, MockedTelnetCommunicator


@pytest.fixture(scope="function")
def reset_singleton():
    """Fixture to reset the singleton instance before each test."""
    TelnetCommunicator._instances = {}
    yield
    TelnetCommunicator._instances = {}


@pytest.fixture
def communicator_class():
    if os.environ.get("HAS_HARDWARE") == "true":
        return TelnetCommunicator
    else:
        return MockedTelnetCommunicator


def test_telnet_communicator_open_close_connection(reset_singleton, communicator_class):
    communicator = communicator_class(host="localhost", port=25000)

    # Try closing
    try:
        communicator.close()
    except Exception as e:
        pytest.fail(f"Closing the connection resulted in an error: {e}")


def test_telnet_communicator_send_invalid_command(reset_singleton, communicator_class):
    expected_response = ["\r", "Error: Unknown command\r", "-501\r", "cmd: "]
    communicator = communicator_class(host="localhost", port=25000)
    # Try sending invalid command
    response = communicator.send_and_receive("bla")
    communicator.close()
    assert response == expected_response


def test_telnet_communicator_send_help(reset_singleton, communicator_class):
    expected_partial_response = [
        "\r",
        "\r",
        "Remote Command Interface Commands:\r",
        " Node Commands\r",
        "    exit                        - Disconnect\r",
    ]
    communicator = communicator_class(host="localhost", port=25000)
    # Try sending valid command
    response = communicator.send_and_receive("help")
    communicator.close()
    # Then the first five elements of the response matches the expected partial response
    assert response[:5] == expected_partial_response
