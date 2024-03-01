import re
from typing import Any, final

from loguru import logger
from overrides import override

from horiba_sdk.communication import Command, Response
from horiba_sdk.icl_error import AbstractErrorDB
from horiba_sdk.sync.communication import AbstractCommunicator
from horiba_sdk.sync.devices.abstract_device_discovery import AbstractDeviceDiscovery
from horiba_sdk.sync.devices.single_devices import ChargeCoupledDevice, Monochromator


@final
class DeviceDiscovery(AbstractDeviceDiscovery):
    def __init__(self, communicator: AbstractCommunicator, error_db: AbstractErrorDB):
        self._communicator: AbstractCommunicator = communicator
        self._charge_coupled_devices: list[ChargeCoupledDevice] = []
        self._monochromators: list[Monochromator] = []
        self._error_db: AbstractErrorDB = error_db
        self._discovered_devices: bool = False

    @override
    def execute(self, error_on_no_device: bool = False) -> None:
        """
        Discovers the connected devices and saves them internally.
        """
        if not self._communicator.opened():
            self._communicator.open()

        # Define the commands and device types in a list of tuples for iteration
        commands_and_types = [('ccd_discover', 'ccd_list', 'CCD'), ('mono_discover', 'mono_list', 'Monochromator')]

        for discover_command, list_command, device_type in commands_and_types:
            response: Response = self._communicator.request_with_response(Command(discover_command, {}))
            if response.results.get('count', 0) == 0 and error_on_no_device:
                raise Exception(f'No {device_type} connected')
            response = self._communicator.request_with_response(Command(list_command, {}))

            # as the responses of ccd_list and mono_list differ, we need to parse them separately
            if device_type == 'CCD':
                raw_device_list = response.results
                self._charge_coupled_devices = self._parse_ccds(raw_device_list)
                logger.info(f'Found {len(self._charge_coupled_devices)} CCD devices: {self._charge_coupled_devices}')
            elif device_type == 'Monochromator':
                raw_device_list = response.results['list']
                self._monochromators = self._parse_monos(raw_device_list)
                logger.info(f'Found {len(self._monochromators)} Monochromator devices: {self._monochromators}')

    def _parse_ccds(self, raw_device_list: dict[str, Any]) -> list[ChargeCoupledDevice]:
        detected_ccds: list[ChargeCoupledDevice] = []
        for key, value in raw_device_list.items():
            logger.debug(f'Parsing CCD: {key} - {value}')
            ccd_index: int = int(key.split(':')[0].replace('index', '').strip())
            ccd_type_match = re.search(r'deviceType: (.*?),', value)
            if not ccd_type_match:
                raise Exception(f'Failed to find ccd type "deviceType" in string "{value}"')
            ccd_type: str = str(ccd_type_match.group(1).strip())

            logger.info(f'Detected CCD: {ccd_type}')
            detected_ccds.append(ChargeCoupledDevice(ccd_index, self._communicator, self._error_db))

        return detected_ccds

    def _parse_monos(self, raw_device_list: dict[str, Any]) -> list[Monochromator]:
        detected_monos = []
        for device_string in raw_device_list:
            mono_index: int = int(device_string.split(';')[0])
            mono_type: str = device_string.split(';')[1]

            logger.info(f'Detected Monochromator: {mono_type}')
            detected_monos.append(Monochromator(mono_index, self._communicator, self._error_db))

        return detected_monos

    @override
    def charge_coupled_devices(self) -> list[ChargeCoupledDevice]:
        return self._charge_coupled_devices

    @override
    def monochromators(self) -> list[Monochromator]:
        return self._monochromators
