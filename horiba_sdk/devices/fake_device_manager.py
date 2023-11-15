import asyncio
import contextlib
from asyncio import AbstractEventLoop, Task
from typing import Any, Optional, final

import websockets
from websockets.legacy.server import WebSocketServerProtocol

from horiba_sdk.communication import AbstractCommunicator
from horiba_sdk.devices import AbstractDeviceManager


@final
class FakeDeviceManager(AbstractDeviceManager):
    """
    The FakeDeviceManager represents a `horiba_sdk.devices.DeviceManager` that
    can be used in the unit tests. It starts a local websocket server and simply
    returns the command that was sent.

    Should be used in a pytest fixture as follows::

        fake_icl_host: str = 'localhost'
        fake_icl_port: int = 8765

        @pytest.fixture(scope='module')
        def _run_fake_icl_server():
            fake_device_manager = FakeDeviceManager(fake_icl_host, fake_icl_port)

            thread = threading.Thread(target=fake_device_manager.start_icl)
            thread.start()
            yield
            fake_device_manager.loop.call_soon_threadsafe(fake_device_manager.server.cancel)
            thread.join()

        @pytest.mark.asyncio
        async def your_unit_test(_run_fake_icl_server):
            pass

    """

    def __init__(self, host: str = '127.0.0.1', port: int = 25011):
        self.host = host
        self.port = port
        self.websocket: Optional[WebSocketServerProtocol] = None
        self.loop: Optional[AbstractEventLoop] = None
        self.server: Optional[Task[Any]] = None

    async def _websocket_server(self) -> None:
        async with websockets.serve(self._echo_handler, self.host, self.port):
            await asyncio.Future()

    def start_icl(self) -> None:
        """
        Starts a local websocket server as an asyncio task in a new async loop.
        Handles the closing of the loop
        """
        self.loop = asyncio.new_event_loop()
        self.server = self.loop.create_task(self._websocket_server())

        with contextlib.suppress(asyncio.CancelledError):
            self.loop.run_until_complete(self.server)

        self.loop.close()

    def stop_icl(self) -> None:
        """
        Does nothing.
        """
        pass

    def discover_devices(self) -> None:
        """
        Does nothing.
        """
        pass

    @staticmethod
    def handle_error(error: Exception) -> None:
        """
        Does nothing.
        """
        pass

    @property
    def communicator(self) -> AbstractCommunicator:
        """
        Does nothing.
        """
        pass

    async def _echo_handler(self, websocket: WebSocketServerProtocol) -> None:
        async for message in websocket:
            await websocket.send(message)
