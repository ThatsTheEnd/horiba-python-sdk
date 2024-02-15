from enum import Enum
from types import TracebackType
from typing import Any, Optional, Union, final

import pint
from loguru import logger
from overrides import override

from horiba_sdk import ureg
from horiba_sdk.communication import AbstractCommunicator, Response
from horiba_sdk.core.resolution import Resolution
from horiba_sdk.icl_error import AbstractErrorDB

from .abstract_device import AbstractDevice


@final
class ChargeCoupledDevice(AbstractDevice):
    """Charge Coupled Device

    This class should not be instanced by the end user. Instead, the :class:`horiba_sdk.devices.DeviceManager`
    should be used to access the detected CCDs on the system.
    """

    @final
    class XAxisConversionType(Enum):
        NONE = 0
        FROM_CCD_FIRMWARE = 1
        FROM_ICL_SETTINGS_INI = 2

    def __init__(self, device_id: int, communicator: AbstractCommunicator, error_db: AbstractErrorDB) -> None:
        super().__init__(device_id, communicator, error_db)

    async def __aenter__(self) -> 'ChargeCoupledDevice':
        await self.open()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException], exc_value: BaseException, traceback: Optional[TracebackType]
    ) -> None:
        is_open = await self.is_open()
        if not is_open:
            logger.debug('CCD is already closed')
            return

        await self.close()

    @override
    async def open(self) -> None:
        """Opens the connection to the Charge Coupled Device

        Raises:
            Exception: When an error occurred on the device side
        """
        await super().open()
        await super()._execute_command('ccd_open', {'index': self._id})

    @override
    async def close(self) -> None:
        """Closes the connection to the ChargeCoupledDevice

        Raises:
            Exception: When an error occurred on the device side
        """
        await super()._execute_command('ccd_close', {'index': self._id})

    async def is_open(self) -> bool:
        """Checks if the connection to the charge coupled device is open.

        Raises:
            Exception: When an error occurred on the device side
        """
        response: Response = await super()._execute_command('ccd_isOpen', {'index': self._id})
        return bool(response.results['open'])

    async def get_temperature(self) -> pint.Quantity:
        """Chip temperature of the CCD.

        Returns:
            pint.Quantity: chip's temperature in degree Celsius

        Raises:
            Exception: When an error occurred on the device side
        """
        response: Response = await super()._execute_command('ccd_getChipTemperature', {'index': self._id})
        return ureg.Quantity(response.results['temperature'], ureg.degC)  # type: ignore

    async def get_chip_size(self) -> Resolution:
        """Chip resolution of the CCD.

        Returns:
            Resolution: chip resolution (width, height)

        Raises:
            Exception: When an error occurred on the device side
        """
        response: Response = await super()._execute_command('ccd_getChipSize', {'index': self._id})
        width: int = response.results['x']
        height: int = response.results['y']
        resolution: Resolution = Resolution(width, height)
        return resolution

    async def get_speed(self) -> Union[pint.Quantity, None]:
        """Chip transfer speed in kHz

        Returns:
            pint.Quantity: Transfer speed in kilo Hertz

        Raises:
            Exception: When an error occurred on the device side
        """
        response: Response = await super()._execute_command('ccd_getSpeed', {'index': self._id})
        return ureg(response.results['info'])

    async def get_exposure_time(self) -> Union[pint.Quantity, None]:
        """Returns the exposure time in ms

        Returns:
            pint.Quantity: Exposure time in ms
        Raises:
            Exception: When an error occurred on the device side
        """
        response: Response = await super()._execute_command('ccd_getExposureTime', {'index': self._id})
        exposure = ureg.Quantity(response.results['time'], 'ms')
        return exposure

    async def set_exposure_time(self, exposure_time_ms: int) -> None:
        """Sets the exposure time in ms

        Args:
            exposure_time_ms (int): Exposure time in ms
        Raises:
            Exception: When an error occurred on the device side
        """

        await super()._execute_command('ccd_setExposureTime', {'index': self._id, 'time': exposure_time_ms})

    async def get_acquisition_ready(self) -> bool:
        """Returns true if the CCD is ready to acquire

        Returns:
            bool: True if the CCD is ready to acquire
        Raises:
            Exception: When an error occurred on the device side
        """
        response: Response = await super()._execute_command('ccd_getAcquisitionReady', {'index': self._id})
        return bool(response.results['ready'])

    async def set_acquisition_start(self, open_shutter: bool) -> None:
        """Starts the acquisition of the CCD

        Args:
            open_shutter (bool): Whether the shutter of the camera should be open
        Raises:
            Exception: When an error occurred on the device side
        """
        await super()._execute_command('ccd_setAcquisitionStart', {'index': self._id, 'openShutter': open_shutter})

    async def set_region_of_interest(
        self,
        roi_index: int = 1,
        x_origin: int = 0,
        y_origin: int = 0,
        x_size: int = 1024,
        y_size: int = 256,
        x_bin: int = 1,
        y_bin: int = 256,
    ) -> None:
        """Sets the region of interest of the CCD
        an example json command looks like this:

        Args:
            roi_index (int, optional): Index of the region of interest. Defaults to 1.
            x_origin (int, optional): X origin of the region of interest. Defaults to 0.
            y_origin (int, optional): Y origin of the region of interest. Defaults to 0.
            x_size (int, optional): X size of the region of interest. Defaults to 1024.
            y_size (int, optional): Y size of the region of interest. Defaults to 256.
            x_bin (int, optional): X bin of the region of interest. Defaults to 1.
            y_bin (int, optional): Y bin of the region of interest. Defaults to 256.

        Raises:
            Exception: When an error occurred on the device side
        """
        await super()._execute_command(
            'ccd_setRoi',
            {
                'index': self._id,
                'roiIndex': roi_index,
                'xOrigin': x_origin,
                'yOrigin': y_origin,
                'xSize': x_size,
                'ySize': y_size,
                'xBin': x_bin,
                'yBin': y_bin,
            },
        )

    async def get_acquisition_data(self) -> dict[Any, Any]:
        """Returns the acquisition data of the CCD
        nina: atm this returns data still formatted for telnet communication, not formatted as json"""
        response: Response = await super()._execute_command('ccd_getAcquisitionData', {'index': self._id})
        return response.results

    async def get_acquisition_busy(self) -> bool:
        """Returns true if the CCD is busy with the acquisition"""
        response: Response = await super()._execute_command('ccd_getAcquisitionBusy', {'index': self._id})
        return bool(response.results['isBusy'])

    async def set_x_axis_conversion_type(self, conversion_type: XAxisConversionType) -> None:
        """Sets the conversion type of the x axis"""
        await super()._execute_command('ccd_setXAxisConversionType', {'index': self._id, 'type': conversion_type.value})

    async def get_x_axis_conversion_type(self) -> XAxisConversionType:
        """Gets the conversion type of the x axis"""
        response: Response = await super()._execute_command('ccd_getXAxisConversionType', {'index': self._id})
        return self.XAxisConversionType(response.results['type'])
