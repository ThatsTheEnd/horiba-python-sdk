from abc import ABC, abstractmethod

from horiba_sdk.communication.abstract_communicator import AbstractCommunicator
from horiba_sdk.devices.abstract_device_manager import AbstractDeviceManager


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

    def __init__(self, id: int, device_manager: AbstractDeviceManager) -> None:
        self._id: int = id
        self._device_manager: AbstractDeviceManager = device_manager
        self._communicator: AbstractCommunicator = device_manager.communicator

    @abstractmethod
    async def open(self) -> None:
        """
        Open a connection to the device.

        Returns:
            Result: Result object indicating success or failure.
        """
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
