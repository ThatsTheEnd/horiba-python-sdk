from abc import ABC, abstractmethod
from typing import Any

from horiba_sdk.communication import WebsocketCommunicator


class AbstractDeviceManager(ABC):
    """
    DeviceManager class manages the lifecycle and interactions with devices.

    """

    def __init__(self, start_icl: bool = True):
        self.binary_messages_enabled: bool = False
        self._start_icl: bool = start_icl

    @abstractmethod
    def start_icl(self) -> None:
        """
        Abstract method that starts the ICL software and establishes communication.
        """
        pass

    @abstractmethod
    def stop_icl(self) -> Any:
        """
        Abstract method that stops the communication and cleans up resources.
        """
        pass

    @abstractmethod
    async def discover_devices(self, error_on_no_device: bool = False) -> None:
        """
        Abstract method that discovers and registers devices.

        Args:
            error_on_no_device (bool): If True, an exception is raised if no device is connected.
        """
        pass

    @abstractmethod
    def handle_errors(self, errors: list[str]) -> None:
        """
        Abstract method that handles errors, logs them, and may take corrective actions.

        Args:
            errors (List[str]): The errors to handle.
        """
        pass

    @property
    @abstractmethod
    def communicator(self) -> WebsocketCommunicator:
        """
        Abstract method to get the communicator attribute.

        Returns:
            AbstractCommunicator: Returns the internal communicator instance.
        """
        pass
