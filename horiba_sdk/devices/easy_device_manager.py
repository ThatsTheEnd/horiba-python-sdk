import asyncio
from typing import Any, Callable, final

from mypy_extensions import KwArg, VarArg

from horiba_sdk.communication import WebsocketCommunicator
from horiba_sdk.devices import DeviceManager


def singleton(cls: type[Any]) -> Callable[[VarArg(Any), KwArg(Any)], Any]:
    """
    Decorator to implement the Singleton pattern.
    """

    _instances: dict[type[Any], Any] = {}

    def get_instance(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return get_instance


@final
@singleton
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

    def start_icl(self) -> None:
        """
        Starts the ICL software and establishes communication.
        """
        self._device_manager.start_icl()

    def stop_icl(self) -> None:
        """
        Stops the communication and cleans up resources.
        """
        return asyncio.run(self._device_manager.stop_icl())

    def discover_devices(self, error_on_no_device: bool = False) -> None:
        """
        Discovers the connected devices and saves them internally.
        Args:
            error_on_no_device (bool): If True, an exception is raised if no device is connected.
        """
        return asyncio.run(self._device_manager.discover_devices(error_on_no_device))

    def handle_errors(self, errors: list[str]) -> None:
        """
        Handles errors, logs them, and may take corrective actions.

        Args:
            errors (Exception): The exception or error to handle.
        """
        return self._device_manager.handle_errors(errors)

    @property
    def communicator(self) -> WebsocketCommunicator:
        """
        Getter method for the communicator attribute.

        Returns:
            horiba_sdk.communication.AbstractCommunicator: Returns a new communicator instance.
        """
        return self._device_manager.communicator
