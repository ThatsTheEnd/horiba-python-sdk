# pylint: skip-file
import pytest

from horiba_sdk.communication import Command, CommunicationException, Response, WebsocketCommunicator


@pytest.mark.asyncio
async def test_websocket_opens(fake_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    # act
    async with WebsocketCommunicator(fake_icl_uri_fixture) as websocket_communicator:
        # assert
        assert websocket_communicator.opened()


@pytest.mark.asyncio
async def test_websocket_with_invalid_address_cannot_open(fake_icl_exe):  # noqa: ARG001
    # arrange
    invalid_address: str = 'wk://255.155.55.5:28412'
    # act
    with pytest.raises(CommunicationException):
        async with WebsocketCommunicator(invalid_address) as websocket_communicator:
            # assert
            assert not websocket_communicator.opened()


@pytest.mark.asyncio
async def test_websocket_open_multiple_times_fails(fake_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    # act
    with pytest.raises(CommunicationException):
        async with WebsocketCommunicator(fake_icl_uri_fixture) as websocket_communicator:
            await websocket_communicator.open()


@pytest.mark.asyncio
async def test_websocket_can_send_command(fake_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    # act
    async with WebsocketCommunicator(fake_icl_uri_fixture) as websocket_communicator:
        command: Command = Command('test_command', {'test': 'some_test'})
        await websocket_communicator.send(command)


@pytest.mark.asyncio
async def test_websocket_can_send_and_receive(fake_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    # act
    async with WebsocketCommunicator(fake_icl_uri_fixture) as websocket_communicator:
        command: Command = Command('test_command', {'test': 'some_test'})
        await websocket_communicator.send(command)
        response: Response = await websocket_communicator.response()

        # assert
        assert response is not None and response.command == command.command


@pytest.mark.asyncio
async def test_websocket_can_close(fake_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    # act
    async with WebsocketCommunicator(fake_icl_uri_fixture) as websocket_communicator:
        opened_before_close = websocket_communicator.opened()

    # assert
    opened_after_close = websocket_communicator.opened()
    assert opened_before_close
    assert not opened_after_close


@pytest.mark.asyncio
async def test_websocket_fails_close_when_already_closed(fake_icl_exe, fake_icl_uri_fixture):  # noqa: ARG001
    # arrange
    # act
    async with WebsocketCommunicator(fake_icl_uri_fixture) as websocket_communicator:
        pass

    # assert
    with pytest.raises(CommunicationException):
        await websocket_communicator.close()
