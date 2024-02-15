import asyncio
import contextlib
import json
import os
from asyncio import AbstractEventLoop, Task
from typing import Any, Optional, final

import websockets
from loguru import logger
from overrides import override
from websockets.legacy.server import WebSocketServerProtocol

from horiba_sdk.communication.websocket_communicator import WebsocketCommunicator
from horiba_sdk.devices.single_devices import ChargeCoupledDevice, Monochromator
from horiba_sdk.icl_error import FakeErrorDB

from .abstract_device_manager import AbstractDeviceManager


@final
class FakeDeviceManager(AbstractDeviceManager):
    """
    The FakeDeviceManager represents a `horiba_sdk.devices.DeviceManager` that can be used in the unit tests. It starts
    a local websocket server and returns the predefined response located in `horiba_sdk/devices/fake_responses/*.json`.
    Currently supported devices for fake responses are:
    - The ICL itself
    - The :class:`Monochromator`

    For other unsupported devices, it just responds with the sent command.

    The class should be used in a pytest fixture as follows::

        fake_icl_host: str = 'localhost'
        fake_icl_port: int = 8765

        @pytest.fixture(scope='module')
        def fake_device_manager():
            fake_device_manager = FakeDeviceManager(fake_icl_host, fake_icl_port)
            return fake_device_manager


        @pytest.fixture(scope='module')
        def _run_fake_icl_server(fake_device_manager):
            thread = threading.Thread(target=fake_device_manager.start_icl)
            thread.start()
            yield
            fake_device_manager.loop.call_soon_threadsafe(fake_device_manager.server.cancel)
            thread.join()

        @pytest.mark.asyncio
            async def your_unit_test(fake_device_manager, _run_fake_icl_server):
            pass

    """

    def __init__(self, host: str = '127.0.0.1', port: int = 25011):
        self.host = host
        self.port = port
        self.websocket: Optional[WebSocketServerProtocol] = None
        self.loop: Optional[AbstractEventLoop] = None
        self.server: Optional[Task[Any]] = None
        self.error_db: FakeErrorDB = FakeErrorDB()

        current_directory = os.path.dirname(__file__)
        fake_responses_path = os.path.join(current_directory, 'fake_responses')

        icl_fake_responses_path = os.path.join(fake_responses_path, 'icl.json')
        with open(icl_fake_responses_path) as json_file:
            self.icl_responses = json.load(json_file)

        monochromator_fake_responses_path = os.path.join(fake_responses_path, 'monochromator.json')
        with open(monochromator_fake_responses_path) as json_file:
            self.monochromator_responses = json.load(json_file)

        ccd_fake_responses_path = os.path.join(fake_responses_path, 'ccd.json')
        with open(ccd_fake_responses_path) as json_file:
            self.ccd_responses = json.load(json_file)

    async def _websocket_server(self) -> None:
        async with websockets.serve(self._echo_handler, self.host, self.port):
            await asyncio.Future()

    def start_fake(self) -> None:
        """
                        Starts a local websocket server as an asyncio task in a new async loop.
                        Handles the closing of the loop
                        """
        self.loop = asyncio.new_event_loop()
        self.server = self.loop.create_task(self._websocket_server())

        with contextlib.suppress(asyncio.CancelledError):
            self.loop.run_until_complete(self.server)

        self.loop.close()

    async def start(self) -> None:
        """
                Starts a local websocket server as an asyncio task in a new async loop.
                Handles the closing of the loop
                """
        self.loop = asyncio.new_event_loop()
        self.server = self.loop.create_task(self._websocket_server())

        with contextlib.suppress(asyncio.CancelledError):
            self.loop.run_until_complete(self.server)

        self.loop.close()

    async def stop(self) -> None:
        """
        Does nothing.
        """
        pass

    @override
    async def discover_devices(self, error_on_no_device: bool = False) -> None:
        """
        Does nothing.
        """
        pass

    @property
    @override
    def communicator(self) -> WebsocketCommunicator:
        """Communicator"""
        return WebsocketCommunicator('ws://' + self.host + ':' + str(self.port))

    @property
    @override
    def monochromators(self) -> list[Monochromator]:
        """
        Abstract method to get the detected monochromators.

        Returns:
            List[Monochromator]: The detected monochromators
        """
        return [Monochromator(0, self.communicator, self.error_db)]

    @property
    @override
    def charge_coupled_devices(self) -> list[ChargeCoupledDevice]:
        """
        Abstract method to get the detected CCDs.

        Returns:
            List[ChargeCoupledDevice]: The detected CCDS.
        """
        return [ChargeCoupledDevice(0, self.communicator, self.error_db)]

    async def _echo_handler(self, websocket: WebSocketServerProtocol) -> None:
        async for message in websocket:
            logger.info('received: {message}', message=message)
            command = json.loads(message)
            if command['command'].startswith('icl_'):
                response = json.dumps(self.icl_responses[command['command']])
                await websocket.send(response)
            elif command['command'].startswith('mono_'):
                response = json.dumps(self.monochromator_responses[command['command']])
                await websocket.send(response)
            elif command['command'].startswith('ccd_'):
                response = json.dumps(self.ccd_responses[command['command']])
                await websocket.send(response)
            else:
                logger.info('unknown command, responding with message')
                await websocket.send(message)
