from abc import ABC, abstractmethod

from horiba_sdk.sync.devices.single_devices import ChargeCoupledDevice, Monochromator


class AbstractDeviceDiscovery(ABC):
    @abstractmethod
    def execute(self, error_on_no_device: bool = False) -> None:
        pass

    @abstractmethod
    def charge_coupled_devices(self) -> list[ChargeCoupledDevice]:
        pass

    @abstractmethod
    def monochromators(self) -> list[Monochromator]:
        pass
