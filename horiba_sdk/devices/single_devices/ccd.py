from types import TracebackType
from typing import Optional, Union, final

import pint
from loguru import logger
from overrides import override

from horiba_sdk import ureg
from horiba_sdk.communication.messages import Command, Response
from horiba_sdk.core.resolution import Resolution
from horiba_sdk.devices.abstract_device_manager import AbstractDeviceManager

from .abstract_device import AbstractDevice


@final
class ChargeCoupledDevice(AbstractDevice):
    """Charge Coupled Device

    Example usage::

        from horiba_sdk.devices.ccd import ChargeCoupledDevice

        # using the context manager:
        with ChargeCoupledDevice(1, device_manager) as ccd:
            print(await ccd.is_open)

        # alternative usage
        ccd: ChargeCoupledDevice = ChargeCoupledDevice(1, device_manager)
        await charge coupled device.open()
        print(await charge coupled device.is_open)
        await charge coupled device.close()

    """

    def __init__(self, id: int, device_manager: AbstractDeviceManager) -> None:
        super().__init__(id, device_manager)

    async def __aenter__(self) -> 'ChargeCoupledDevice':
        await self.open()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException], exc_value: BaseException, traceback: Optional[TracebackType]
    ) -> None:
        await self.close()

    @override
    async def open(self) -> None:
        """Opens the connection to the Charge Coupled Device

        Raises:
            Exception: When an error occured on the device side
        """
        await super().open()

        command = Command('ccd_discover', {})
        await self._communicator.send(command)
        response = await self._communicator.response()

        if response.errors:
            self._device_manager.handle_errors(response.errors)
            raise Exception(f'ChargeCoupledDevice encountered error: {response.errors}')
        if response.results['count'] == 0:
            raise Exception('No ChargeCoupledDevice connected')

        command = Command('ccd_open', {'index': self._id})
        await self._communicator.send(command)
        _ignored_response = await self._communicator.response()

        if _ignored_response.errors:
            self._device_manager.handle_errors(_ignored_response.errors)
            raise Exception(f'ChargeCoupledDevice encountered error: {_ignored_response.errors}')

    @override
    async def close(self) -> None:
        """Closes the connection to the ChargeCoupledDevice

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('ccd_close', {'index': self._id})
        await self._communicator.send(command)
        _ignored_response = await self._communicator.response()
        await super().close()

        if _ignored_response.errors:
            self._device_manager.handle_errors(_ignored_response.errors)
            raise Exception(f'ChargeCoupledDevice encountered error: {_ignored_response.errors}')

    @property
    async def is_open(self) -> bool:
        """Checks if the connection to the charge coupled device is open.

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('ccd_isOpen', {'index': self._id})
        await self._communicator.send(command)
        response: Response = await self._communicator.response()
        if response.errors:
            self._device_manager.handle_errors(response.errors)
            raise Exception(f'ChargeCoupledDevice encountered error: {response.errors}')
        logger.debug(f'CCD {self._id} is open: {bool(response.results["open"])}')
        return bool(response.results['open'])

    @property
    async def temperature(self) -> pint.Quantity:
        """Chip temperature of the CCD.

        Returns:
            pint.Quantity: chip's temperature in degree Celsius

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('ccd_getChipTemperature', {'index': self._id})
        await self._communicator.send(command)
        response: Response = await self._communicator.response()
        if response.errors:
            self._device_manager.handle_errors(response.errors)
            raise Exception(f'ChargeCoupledDevice encountered error: {response.errors}')

        return ureg.Quantity(response.results['temperature'], ureg.degC)  # type: ignore

    @property
    async def resolution(self) -> Resolution:
        """Chip resolution of the CCD.

        Returns:
            Resolution: chip resolution (width, height)

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('ccd_getChipSize', {'index': self._id})
        await self._communicator.send(command)
        response: Response = await self._communicator.response()
        if response.errors:
            self._device_manager.handle_errors(response.errors)
            raise Exception(f'ChargeCoupledDevice encountered error: {response.errors}')

        width: int = response.results['x']
        height: int = response.results['y']
        resolution: Resolution = Resolution(width, height)
        return resolution

    @property
    async def speed(self) -> Union[pint.Quantity, None]:
        """Chip transfer speed in kHz

        Returns:
            pint.Quantity: Transfer speed in kilo Herz

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('ccd_getSpeed', {'index': self._id})
        await self._communicator.send(command)
        response: Response = await self._communicator.response()
        if response.errors:
            self._device_manager.handle_errors(response.errors)
            raise Exception(f'ChargeCoupledDevice encountered error: {response.errors}')

        return ureg(response.results['info'])

    async def get_exposure_time(self) -> Union[pint.Quantity, None]:
        """Returns the exposure time in ms

        Returns:
            pint.Quantity: Exposure time in ms
        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('ccd_getExposureTime', {'index': self._id})
        await self._communicator.send(command)
        response: Response = await self._communicator.response()
        if response.errors:
            self._device_manager.handle_errors(response.errors)
            raise Exception(f'ChargeCoupledDevice encountered error: {response.errors}')

        exposure = ureg.Quantity(response.results['time'], 'ms')
        logger.debug(f'CCD {self._id} exposure time: {exposure}')
        return exposure

    async def set_exposure_time(self, exposure_time_ms: int) -> None:
        """Sets the exposure time in ms

        Args:
            exposure_time_ms (int): Exposure time in ms
        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('ccd_setExposureTime', {'index': self._id, 'time': exposure_time_ms})
        await self._communicator.send(command)
        response: Response = await self._communicator.response()
        if response.errors:
            self._device_manager.handle_errors(response.errors)
            raise Exception(f'ChargeCoupledDevice encountered error: {response.errors}')

    async def set_acquisition_start(self) -> None:
        """Starts the acquisition of the CCD
        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('ccd_setAcquisitionStart', {'index': self._id})
        await self._communicator.send(command)
        response: Response = await self._communicator.response()
        if response.errors:
            self._device_manager.handle_errors(response.errors)
            raise Exception(f'ChargeCoupledDevice encountered error: {response.errors}')
