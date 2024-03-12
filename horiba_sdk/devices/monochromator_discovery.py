from typing import Any, final

from loguru import logger
from overrides import override

from horiba_sdk.communication import AbstractCommunicator, Command, Response
from horiba_sdk.devices.abstract_device_discovery import AbstractDeviceDiscovery
from horiba_sdk.devices.single_devices import Monochromator
from horiba_sdk.icl_error import AbstractErrorDB


@final
class MonochromatorsDiscovery(AbstractDeviceDiscovery):
    def __init__(self, communicator: AbstractCommunicator, error_db: AbstractErrorDB):
        self._communicator: AbstractCommunicator = communicator
        self._monochromators: list[Monochromator] = []
        self._error_db: AbstractErrorDB = error_db

    @override
    async def execute(self, error_on_no_device: bool = False) -> None:
        """
        Discovers the connected Monochromators and saves them internally.
        """
        if not self._communicator.opened():
            await self._communicator.open()

        response: Response = await self._communicator.request_with_response(Command('mono_discover', {}))
        if response.results.get('count', 0) == 0 and error_on_no_device:
            raise Exception('No Monochromators connected')

        response = await self._communicator.request_with_response(Command('mono_list', {}))
        raw_device_list = response.results['list']
        self._monochromators = self._parse_monos(raw_device_list)
        logger.info(f'Found {len(self._monochromators)} Monochromator devices: {self._monochromators}')

    def _parse_monos(self, raw_device_list: dict[str, Any]) -> list[Monochromator]:
        detected_monos = []
        for device_string in raw_device_list:
            mono_index: int = int(device_string.split(';')[0])
            mono_type: str = device_string.split(';')[1]

            logger.info(f'Detected Monochromator: {mono_type}')
            detected_monos.append(Monochromator(mono_index, self._communicator, self._error_db))

        return detected_monos

    def monochromators(self) -> list[Monochromator]:
        return self._monochromators
