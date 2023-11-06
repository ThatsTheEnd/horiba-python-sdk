from abc import ABC, abstractmethod

from horiba_sdk.communication import AbstractCommunicator


class AbstractDeviceManager(ABC):
    """
    DeviceManager class manages the lifecycle and interactions with devices.

    Attributes:
        _communicator (AbstractCommunicator): The communicator class used to talk to devices.
        devices (List[Device]): List of managed devices.
    """

    @abstractmethod
    def start_icl(self) -> None:
        """
        Abstract method that starts the ICL software and establishes communication.
        """
        pass

    @abstractmethod
    def stop_icl(self) -> None:
        """
        Abstract method that stops the communication and cleans up resources.
        """
        pass

    @abstractmethod
    def discover_devices(self) -> None:
        """
        Abstract method that discovers and registers devices.
        """
        pass

    @staticmethod
    @abstractmethod
    def handle_error(error: Exception) -> None:
        """
        Abstract method that handles errors, logs them, and may take corrective actions.

        Args:
            error (Exception): The exception or error to handle.
        """
        pass

    @property
    @abstractmethod
    def communicator(self) -> AbstractCommunicator:
        """
        Abstract method to get the communicator attribute.

        Returns:
            AbstractCommunicator: Returns the internal communicator instance.
        """
        pass
