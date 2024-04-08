from typing import final

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

            for device in response.results['devices']:
                if device_type == 'CCD':
                    ccd = ChargeCoupledDevice(device['index'], self._communicator, self._error_db)
                    logger.info(f'Detected CCD: {device["deviceType"]}')
                    self._charge_coupled_devices.append(ccd)
                elif device_type == 'Monochromator':
                    mono = Monochromator(device['index'], self._communicator, self._error_db)
                    logger.info(f'Detected Monochromator: {device["deviceType"]}')
                    self._monochromators.append(mono)

        logger.info(f'Found {len(self._monochromators)} Monochromator devices')
        logger.info(f'Found {len(self._charge_coupled_devices)} CCD devices')

    @override
    def charge_coupled_devices(self) -> list[ChargeCoupledDevice]:
        return self._charge_coupled_devices

    @override
    def monochromators(self) -> list[Monochromator]:
        return self._monochromators
