from typing import Any, final

from loguru import logger
from overrides import override

from horiba_sdk.communication import AbstractCommunicator, Command, Response
from horiba_sdk.devices.abstract_device_discovery import AbstractDeviceDiscovery
from horiba_sdk.devices.single_devices import ChargeCoupledDevice
from horiba_sdk.icl_error import AbstractErrorDB


@final
class ChargeCoupledDevicesDiscovery(AbstractDeviceDiscovery):
    def __init__(self, communicator: AbstractCommunicator, error_db: AbstractErrorDB):
        self._communicator: AbstractCommunicator = communicator
        self._charge_coupled_devices: list[ChargeCoupledDevice] = []
        self._error_db: AbstractErrorDB = error_db

    @override
    async def execute(self, error_on_no_device: bool = False) -> None:
        """
        Discovers the connected devices and saves them internally.

        Raises:
            Exception: When no CCDs are discovered and that `error_on_no_device` is set. Or when there is an issue
            parsing the CCD list
        """
        if not self._communicator.opened():
            await self._communicator.open()

        response: Response = await self._communicator.request_with_response(Command('ccd_discover', {}))
        if response.results.get('count', 0) == 0 and error_on_no_device:
            raise Exception('No CCDs connected')

        response = await self._communicator.request_with_response(Command('ccd_list', {}))

        raw_device_list = response.results
        self._charge_coupled_devices = self._parse_ccds(raw_device_list)
        logger.info(f'Found {len(self._charge_coupled_devices)} CCD devices')

    def _parse_ccds(self, raw_device_list: dict[str, Any]) -> list[ChargeCoupledDevice]:
        detected_ccds: list[ChargeCoupledDevice] = []
        for device in raw_device_list['devices']:
            try:
                logger.debug(f'Parsing CCD: {device}')
                ccd = ChargeCoupledDevice(device['index'], self._communicator, self._error_db)
                logger.info(f'Detected CCD: {device["deviceType"]}')
                detected_ccds.append(ccd)
            except Exception as e:
                logger.error(f'Error while parsing ChargeCoupledDevice: {e}')

        return detected_ccds

    def charge_coupled_devices(self) -> list[ChargeCoupledDevice]:
        return self._charge_coupled_devices
