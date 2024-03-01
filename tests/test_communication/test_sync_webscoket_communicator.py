# pylint: skip-file
import time

import pytest

from horiba_sdk.communication import Command, CommunicationException, Response
from horiba_sdk.sync.communication.websocket_communicator import WebsocketCommunicator


def test_websocket_opens(fake_sync_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    websocket_communicator = WebsocketCommunicator(fake_icl_uri_fixture)
    # act
    websocket_communicator.open()
    # assert
    assert websocket_communicator.opened()

    websocket_communicator.close()


def test_websocket_with_invalid_address_cannot_open(fake_sync_icl_exe):  # noqa: ARG001
    # arrange
    invalid_address: str = 'tk:/2255.155.55.5:28412'
    websocket_communicator = WebsocketCommunicator(uri=invalid_address)
    # act
    with pytest.raises(CommunicationException):
        websocket_communicator.open()
        # assert
        assert not websocket_communicator.opened()


def test_websocket_open_multiple_times_fails(fake_sync_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    websocket_communicator = WebsocketCommunicator(fake_icl_uri_fixture)
    # act
    websocket_communicator.open()
    with pytest.raises(CommunicationException):
        websocket_communicator.open()

    websocket_communicator.close()


def test_websocket_can_send_command(fake_sync_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    websocket_communicator = WebsocketCommunicator(fake_icl_uri_fixture)
    websocket_communicator.open()

    # act
    command: Command = Command('test_command', {'test': 'some_test'})
    websocket_communicator.send(command)

    websocket_communicator.close()


def test_websocket_can_send_and_receive(fake_sync_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    websocket_communicator = WebsocketCommunicator(fake_icl_uri_fixture)
    websocket_communicator.open()

    # act
    command: Command = Command('test_command', {'test': 'some_test'})
    websocket_communicator.send(command)
    time.sleep(0.1)
    response: Response = websocket_communicator.response()

    # assert
    assert response is not None and response.command == command.command

    websocket_communicator.close()


def test_websocket_request_with_response(fake_sync_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    websocket_communicator = WebsocketCommunicator(fake_icl_uri_fixture)
    websocket_communicator.open()

    # act
    command: Command = Command('test_command', {'test': 'some_test'})
    response: Response = websocket_communicator.request_with_response(command)

    # assert
    assert response is not None and response.command == command.command

    websocket_communicator.close()


def test_websocket_request_with_response_with_context_manager(fake_sync_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    # act
    with WebsocketCommunicator(fake_icl_uri_fixture) as websocket_communicator:
        command: Command = Command('test_command', {'test': 'some_test'})
        response: Response = websocket_communicator.request_with_response(command)

    # assert
    assert response is not None and response.command == command.command


def test_websocket_can_close(fake_sync_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    websocket_communicator = WebsocketCommunicator(fake_icl_uri_fixture)
    websocket_communicator.open()

    # act
    opened_before_close = websocket_communicator.opened()
    websocket_communicator.close()

    # assert
    opened_after_close = websocket_communicator.opened()
    assert opened_before_close
    assert not opened_after_close


def test_websocket_fails_close_when_already_closed(fake_sync_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    websocket_communicator = WebsocketCommunicator(fake_icl_uri_fixture)

    # act
    websocket_communicator.open()
    websocket_communicator.close()

    # assert
    with pytest.raises(CommunicationException):
        websocket_communicator.close()
