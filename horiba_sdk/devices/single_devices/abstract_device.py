from abc import ABC, abstractmethod
from typing import Any

from horiba_sdk.communication import Response, WebsocketCommunicator
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

    def __init__(self, device_manager: AbstractDeviceManager) -> None:
        self._id: int = -1
        self._device_manager: AbstractDeviceManager = device_manager
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

    async def _execute_command(self, command_name: str, parameters: dict[Any, Any]) -> Response:
        """
        Creates a command from the command name, and it's parameters
        Executes a command and handles the response.

        Args:
            command_name (str): The name of the command to execute.
            parameters (dict): The parameters for the command.

        Returns:
            Response: The response from the device.

        Raises:
            Exception: When an error occurred on the device side.
        """
        response: Response = await self._communicator.execute_command(command_name, parameters)
        if response.errors:
            self._device_manager.handle_errors(response.errors)
            raise Exception(f'Encountered error: {response.errors}')
        return response
