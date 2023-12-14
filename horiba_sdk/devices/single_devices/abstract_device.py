from abc import ABC, abstractmethod

from horiba_sdk.communication import WebsocketCommunicator
from horiba_sdk.devices.device_manager import DeviceManager


class AbstractDevice(ABC):
    """
    Abstract base class representing a generic device.

    This class provides an interface for device-specific operations.
    Concrete implementations should provide specific functionalities
    for each of the abstract methods.
    """

    def __init__(self, device_manager: DeviceManager, device_id: int) -> None:
        # Assuming you might want some kind of initialization here.
        # This can be expanded as needed.
        self._device_manager: DeviceManager = device_manager
        self._communicator: WebsocketCommunicator = device_manager.communicator
        self._device_id = device_id

    @abstractmethod
    def _open(self) -> None:
        """
        Open a connection to the device.

        Returns:
            Result: Result object indicating success or failure.
        """
        pass

    @abstractmethod
    def _close(self) -> None:
        """
        Close the connection to the device.

        Returns:
            Result: Result object indicating success or failure.
        """
        pass
