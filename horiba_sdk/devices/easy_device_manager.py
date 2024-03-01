import asyncio
from typing import final

from horiba_sdk.communication import AbstractCommunicator
from horiba_sdk.devices import DeviceManager
from horiba_sdk.devices.single_devices import EasyCCD, Monochromator


@final
class EasyDeviceManager:
    """
    This class provides a synchronous interface to the DeviceManager class.
    It was created to allow users who are not familiar with asynchronous programming
    to use the DeviceManager class in a synchronous manner.

    Each method in this class wraps a corresponding method in the DeviceManager
    class with asyncio.run(), which runs the method in a blocking manner.

    Note: This class should be used in scripts or applications that are not already
    running an event loop. If an event loop is already running, the asyncio.run()
    calls will raise an error.

    Attributes:
        start_icl: bool = True: immediately start the ICL or not
        websocket_ip: str = '127.0.0.1': websocket IP
        websocket_port: str = '25010': websocket port
    """

    def __init__(self, start_icl: bool = True, websocket_ip: str = '127.0.0.1', websocket_port: str = '25010'):
        """
        Initializes the DeviceManager with the specified communicator class.

        Args:
            start_icl: bool = True: immediately start the ICL or not
            websocket_ip: str = '127.0.0.1': websocket IP
            websocket_port: str = '25010': websocket port
        """
        self._device_manager = DeviceManager(start_icl, websocket_ip, websocket_port)
        self._easy_ccds = []
        self._easy_monos = []

    def start(self) -> None:
        """
        Starts the device manager.
        """
        asyncio.run(self._device_manager.start())
        self.discover_devices()

    def stop(self) -> None:
        """
        Stops the device manager.
        """
        return asyncio.run(self._device_manager.stop())

    def discover_devices(self, error_on_no_device: bool = False) -> None:
        """
        Discovers the connected devices and saves them internally.
        Args:
            error_on_no_device (bool): If True, an exception is raised if no device is connected.
        """
        asyncio.run(self._device_manager.discover_devices(error_on_no_device))

        for ccd in self._device_manager.charge_coupled_devices:
            self._easy_ccds.append(EasyCCD(ccd))


    @property
    def communicator(self) -> AbstractCommunicator:
        """
        Getter method for the communicator attribute.

        Returns:
            horiba_sdk.communication.AbstractCommunicator: Returns a new communicator instance.
        """
        return self._device_manager.communicator

    @property
    def monochromators(self) -> list[Monochromator]:
        """
        The detected monochromators, should be called after :meth:`discover_devices`

        .. todo:: create EasyMonochromator class
        Returns:
            List[Monochromator]: The detected monochromators
        """
        return self._easy_monos

    @property
    def charge_coupled_devices(self) -> list[EasyCCD]:
        """
        The detected CCDs, should be called after :meth:`discover_devices`

        Returns:
            List[EasyCCD]: The detected CCDS.
        """
        return self._easy_ccds
