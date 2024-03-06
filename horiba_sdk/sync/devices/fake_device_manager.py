from typing import final

from overrides import override

from horiba_sdk.icl_error import FakeErrorDB
from horiba_sdk.sync.communication.websocket_communicator import WebsocketCommunicator
from horiba_sdk.sync.devices.abstract_device_manager import AbstractDeviceManager
from horiba_sdk.sync.devices.single_devices import ChargeCoupledDevice, Monochromator


@final
class FakeDeviceManager(AbstractDeviceManager):
    """
    The FakeDeviceManager represents a `horiba_sdk.sync.devices.DeviceManager` that can be used in the unit tests.

    The class should be used in a pytest fixture as follows::

        fake_icl_host: str = 'localhost'
        fake_icl_port: int = 8765

        @pytest.fixture(scope='module')
        def fake_sync_icl_exe():  # noqa: ARG001
            sync_server = FakeSyncICLServer(fake_icl_host=fake_icl_host, fake_icl_port=fake_icl_port)
            thread = threading.Thread(target=sync_server.start)
            thread.start()

            yield thread

            sync_server.stop()
            thread.join()


        @pytest.fixture(scope='module')
        def fake_sync_device_manager():  # noqa: ARG001
            fake_device_manager = FakeSyncDeviceManager(host=fake_icl_host, port=fake_icl_port)
            fake_device_manager.start()

            yield fake_device_manager
            fake_device_manager.stop()

        def your_unit_test(fake_sync_icl_exe, fake_sync_device_manager):
            pass

    """

    def __init__(self, host: str = '127.0.0.1', port: int = 25011):
        self.host = host
        self.port = port
        self.error_db: FakeErrorDB = FakeErrorDB()
        self.websocket_communicator = WebsocketCommunicator('ws://' + self.host + ':' + str(self.port))

    def start(self) -> None:
        self.websocket_communicator.open()

    def stop(self) -> None:
        self.websocket_communicator.close()

    @override
    def discover_devices(self, error_on_no_device: bool = False) -> None:
        """
        Does nothing.
        """
        pass

    @property
    @override
    def communicator(self) -> WebsocketCommunicator:
        """Communicator"""
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
