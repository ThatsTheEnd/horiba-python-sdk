from typing import final

from overrides import override

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
        # self.websocket: Optional[WebSocketServerProtocol] = None
        self.error_db: FakeErrorDB = FakeErrorDB()
        self.websocket_communicator = WebsocketCommunicator('ws://' + self.host + ':' + str(self.port))

    #         current_directory = os.path.dirname(__file__)
    #         fake_responses_path = os.path.join(current_directory, 'fake_responses')

    #         icl_fake_responses_path = os.path.join(fake_responses_path, 'icl.json')
    #         with open(icl_fake_responses_path) as json_file:
    #             self.icl_responses = json.load(json_file)

    #         monochromator_fake_responses_path = os.path.join(fake_responses_path, 'monochromator.json')
    #         with open(monochromator_fake_responses_path) as json_file:
    #             self.monochromator_responses = json.load(json_file)

    #         ccd_fake_responses_path = os.path.join(fake_responses_path, 'ccd.json')
    #         with open(ccd_fake_responses_path) as json_file:
    #             self.ccd_responses = json.load(json_file)

    async def start(self) -> None:
        """
        Does nothing.
        """
        await self.websocket_communicator.open()

    async def stop(self) -> None:
        """
        Does nothing.
        """
        await self.websocket_communicator.close()

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
        # return WebsocketCommunicator('ws://' + self.host + ':' + str(self.port))
        return self.websocket_communicator

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

    # async def _echo_handler(self, websocket: WebSocketServerProtocol) -> None:
    #     async for message in websocket:
    #         logger.info('received: {message}', message=message)
    #         command = json.loads(message)
    #         if command['command'].startswith('icl_'):
    #             response = json.dumps(self.icl_responses[command['command']])
    #             await websocket.send(response)
    #         elif command['command'].startswith('mono_'):
    #             response = json.dumps(self.monochromator_responses[command['command']])
    #             await websocket.send(response)
    #         elif command['command'].startswith('ccd_'):
    #             response = json.dumps(self.ccd_responses[command['command']])
    #             await websocket.send(response)
    #         else:
    #             logger.info('unknown command, responding with message')
    #             await websocket.send(message)
