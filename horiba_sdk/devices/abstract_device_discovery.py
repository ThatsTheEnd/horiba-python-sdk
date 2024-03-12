from abc import ABC, abstractmethod


class AbstractDeviceDiscovery(ABC):
    @abstractmethod
    async def execute(self, error_on_no_device: bool = False) -> None:
        pass
