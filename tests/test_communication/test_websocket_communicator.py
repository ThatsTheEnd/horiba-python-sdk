# pylint: skip-file
import threading

import pytest

from horiba_sdk.communication import CommunicationException, WebsocketCommunicator
from horiba_sdk.devices import FakeDeviceManager

fake_icl_host: str = 'localhost'
fake_icl_port: int = 8765
fake_icl_uri: str = 'ws://' + fake_icl_host + ':' + str(fake_icl_port)


@pytest.fixture(scope='module')
def _run_fake_icl_server():
    fake_device_manager = FakeDeviceManager(fake_icl_host, fake_icl_port)

    thread = threading.Thread(target=fake_device_manager.start_icl)
    thread.start()
    yield
    fake_device_manager.loop.call_soon_threadsafe(fake_device_manager.server.cancel)
    thread.join()


@pytest.mark.asyncio
async def test_websocket_opens(_run_fake_icl_server):
    # arrange
    websocket_communicator: WebsocketCommunicator = WebsocketCommunicator(fake_icl_uri)

    # act
    async with websocket_communicator:
        # assert
        assert websocket_communicator.opened()


@pytest.mark.asyncio
async def test_websocket_with_invalid_address_cannot_open(_run_fake_icl_server):
    # arrange
    invalid_address: str = 'wk://255.155.55.5:28412'
    websocket_communicator: WebsocketCommunicator = WebsocketCommunicator(invalid_address)

    # act
    # assert
    with pytest.raises(CommunicationException):
        async with websocket_communicator:
            assert not websocket_communicator.opened()


@pytest.mark.asyncio
async def test_websocket_open_multiple_times_fails(_run_fake_icl_server):
    # arrange
    websocket_communicator: WebsocketCommunicator = WebsocketCommunicator(fake_icl_uri)

    # act
    with pytest.raises(CommunicationException):
        async with websocket_communicator:
            await websocket_communicator.open()


@pytest.mark.asyncio
async def test_websocket_can_send_command(_run_fake_icl_server):
    # arrange
    websocket_communicator: WebsocketCommunicator = WebsocketCommunicator(fake_icl_uri)

    # act
    async with websocket_communicator:
        request: str = '{"test": "some test"}'
        await websocket_communicator.send(request)


@pytest.mark.asyncio
async def test_websocket_fails_to_send_message_with_unsupported_type(_run_fake_icl_server):
    # arrange
    websocket_communicator: WebsocketCommunicator = WebsocketCommunicator(fake_icl_uri)

    # act
    async with websocket_communicator:
        # assert
        with pytest.raises(CommunicationException):
            await websocket_communicator.send(123456)


@pytest.mark.asyncio
async def test_websocket_can_receive(_run_fake_icl_server):
    # arrange
    websocket_communicator: WebsocketCommunicator = WebsocketCommunicator(fake_icl_uri)

    # act
    async with websocket_communicator:
        request: str = '{"test": "some test"}'
        await websocket_communicator.send(request)
        response = await websocket_communicator.response()

        # assert
        assert response is not None and response == request


@pytest.mark.asyncio
async def test_websocket_can_send_andreceive(_run_fake_icl_server):
    # arrange
    websocket_communicator: WebsocketCommunicator = WebsocketCommunicator(fake_icl_uri)

    # act
    async with websocket_communicator:
        request: str = '{"test": "some test"}'
        response = await websocket_communicator.send_and_receive(request)

        # assert
        assert response is not None and response == request


@pytest.mark.asyncio
async def test_websocket_can_close(_run_fake_icl_server):
    # arrange
    websocket_communicator: WebsocketCommunicator = WebsocketCommunicator(fake_icl_uri)

    # act
    async with websocket_communicator:
        opened_before_close = websocket_communicator.opened()

    # assert
    opened_after_close = websocket_communicator.opened()
    assert opened_before_close
    assert not opened_after_close


@pytest.mark.asyncio
async def test_websocket_fails_close_when_already_closed(_run_fake_icl_server):
    # arrange
    websocket_communicator: WebsocketCommunicator = WebsocketCommunicator(fake_icl_uri)

    # act
    async with websocket_communicator:
        pass

    # assert
    with pytest.raises(CommunicationException):
        await websocket_communicator.close()
