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

        Raises:
            Exception: When no Monochromators are discovered and that `error_on_no_device` is set. Or when there is an
            issue parsing the Monochromators list
        """
        if not self._communicator.opened():
            await self._communicator.open()

        response: Response = await self._communicator.request_with_response(Command('mono_discover', {}))
        if response.results.get('count', 0) == 0 and error_on_no_device:
            raise Exception('No Monochromators connected')

        response = await self._communicator.request_with_response(Command('mono_list', {}))

        raw_device_list = response.results
        self._monochromators = self._parse_monos(raw_device_list)
        logger.info(f'Found {len(self._monochromators)} Monochromator devices')

    def _parse_monos(self, raw_device_list: dict[str, Any]) -> list[Monochromator]:
        detected_monos: list[Monochromator] = []
        for device in raw_device_list['devices']:
            try:
                logger.debug(f'Parsing Monochromator: {device}')
                mono = Monochromator(device['index'], self._communicator, self._error_db)
                logger.info(f'Detected Monochromator: {device["deviceType"]}')
                detected_monos.append(mono)
            except Exception as e:
                logger.error(f'Error while parsing Monochromator: {e}')

        return detected_monos

    def monochromators(self) -> list[Monochromator]:
        return self._monochromators
