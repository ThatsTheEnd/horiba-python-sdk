from types import TracebackType
from typing import Any, Optional, Union, final

import pint
from overrides import override

from horiba_sdk import ureg
from horiba_sdk.communication import Response
from horiba_sdk.core.resolution import Resolution
from horiba_sdk.devices.device_manager import DeviceManager

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

    def __init__(self, device_manager: DeviceManager) -> None:
        super().__init__(device_manager)
        self.device_list: list[str] = []

    async def __aenter__(self) -> 'ChargeCoupledDevice':
        return self

    async def __aexit__(
        self, exc_type: type[BaseException], exc_value: BaseException, traceback: Optional[TracebackType]
    ) -> None:
        await self.close()

    @override
    async def open(self, device_id: int, enable_binary_messages: bool = True) -> None:
        """Opens the connection to the Charge Coupled Device
        and also sends the command to enable binary messages.
        This is necessary because atm the measurement results
        are sent back as binary messages.

        Raises:
            Exception: When an error occurred on the device side
        """
        await super().open(device_id)
        await super()._execute_command('ccd_open', {'index': self._id})
        if enable_binary_messages:
            await self.do_enable_binary_message()

    async def do_enable_binary_message(self) -> None:
        """Requests the ICL to include binary messages into the communication"""
        await super()._execute_command('icl_binMode', {'mode': 'all'})

    @override
    async def close(self) -> None:
        """Closes the connection to the ChargeCoupledDevice

        Raises:
            Exception: When an error occurred on the device side
        """
        await super()._execute_command('ccd_close', {'index': self._id})
        await super().close()

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
        return bool(response.results['size'])

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
