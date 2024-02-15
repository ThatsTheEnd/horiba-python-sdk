from abc import ABC, abstractmethod

from horiba_sdk.communication import AbstractCommunicator
from horiba_sdk.devices.single_devices import ChargeCoupledDevice, Monochromator


class AbstractDeviceManager(ABC):
    """
    DeviceManager class manages the lifecycle and interactions with devices.

    """

    @abstractmethod
    async def start(self) -> None:
        """
        Abstract method to start the device manager.
        """
        pass

    @abstractmethod
    async def stop(self) -> None:
        """
        Abstract method to stop the device manager.
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

    @property
    @abstractmethod
    def communicator(self) -> AbstractCommunicator:
        """
        Abstract method to get the communicator attribute.

        Returns:
            AbstractCommunicator: Returns the internal communicator instance.
        """
        pass

    @property
    @abstractmethod
    def monochromators(self) -> list[Monochromator]:
        """
        Abstract method to get the detected monochromators.

        Returns:
            List[Monochromator]: The detected monochromators
        """
        pass

    @property
    @abstractmethod
    def charge_coupled_devices(self) -> list[ChargeCoupledDevice]:
        """
        Abstract method to get the detected CCDs.

        Returns:
            List[ChargeCoupledDevice]: The detected CCDS.
        """
        pass
