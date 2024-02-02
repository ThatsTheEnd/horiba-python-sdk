from abc import ABC, abstractmethod

from horiba_sdk.communication.websocket_communicator import WebsocketCommunicator
from horiba_sdk.devices.device_manager import DeviceManager


class AbstractDevice(ABC):
    """
    Abstract base class representing a generic device.

    This class provides an interface for device-specific operations. Concrete implementations should provide specific
    functionalities for each of the abstract methods.

    Attributes:
        _id (int):
        _communicator (WebsocketCommunicator):
        _device_manager (DeviceManager):
    """

    def __init__(self, device_manager: DeviceManager) -> None:
        self._id: int = -1
        self._device_manager: DeviceManager = device_manager
        self._communicator: WebsocketCommunicator = device_manager.communicator

    @abstractmethod
    async def open(self, device_id: int) -> None:
        """
        Open a connection to the device.

        Returns:
            Result: Result object indicating success or failure.
        """
        self._id = device_id
        if not self._communicator.opened():
            await self._communicator.open()

    @abstractmethod
    async def close(self) -> None:
        """
        Close the connection to the device.

        Returns:
            Result: Result object indicating success or failure.
        """
        if self._communicator.opened():
            await self._communicator.close()
