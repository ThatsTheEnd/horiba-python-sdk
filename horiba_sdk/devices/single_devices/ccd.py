from types import TracebackType
from typing import List, Optional, Union, final

import inspect
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

    def __init__(self, ccd_id: int, device_manager: AbstractDeviceManager) -> None:
        super().__init__(ccd_id, device_manager)

    async def __aenter__(self) -> 'ChargeCoupledDevice':
        await self.open()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException], exc_value: BaseException, traceback: Optional[TracebackType]
    ) -> None:
        await self.close()

    async def _execute_command(self, command_name: str, parameters: dict) -> Response:
        """
        Creates a command from the command name, and it's parameters
        Executes a command and handles the response.

        Args:
            command_name (str): The name of the command to execute.
            parameters (dict): The parameters for the command.

        Returns:
            Response: The response from the device.

        Raises:
            Exception: When an error occurred on the device side.
        """
        command = Command(command_name, parameters)  # create command
        await self._communicator.send(command)  # send command
        response = await self._communicator.response()  # get response
        if response.errors:  # handle errors
            self._device_manager.handle_errors(response.errors)
            raise Exception(f'{self._get_caller_name()} encountered error: {response.errors}')
        return response

    @override
    async def open(self) -> None:
        """Opens the connection to the Charge Coupled Device
        and also sends the command to enable binary messages.
        This is necessary because atm the measurement results
        are sent back as binary messages.

        Raises:
            Exception: When an error occurred on the device side
        """
        await super().open()
        response: Response = await self._execute_command('ccd_discover', {})
        if response.results['count'] == 0:
            raise Exception('No ChargeCoupledDevice connected')
        await self._execute_command('ccd_open', {'index': self._id})

    async def do_enable_binary_message(self) -> None:
        """Requests the ICL to include binary messages into the communication
        """
        await self._execute_command('icl_binMode', {'mode': 'all'})

    @override
    async def close(self) -> None:
        """Closes the connection to the ChargeCoupledDevice

        Raises:
            Exception: When an error occurred on the device side
        """
        await self._execute_command('ccd_close', {'index': self._id})
        await super().close()

    async def is_open(self) -> bool:
        """Checks if the connection to the charge coupled device is open.

        Raises:
            Exception: When an error occurred on the device side
        """
        response: Response = await self._execute_command('ccd_isOpen', {'index': self._id})
        return bool(response.results['open'])

    async def get_temperature(self) -> pint.Quantity:
        """Chip temperature of the CCD.

        Returns:
            pint.Quantity: chip's temperature in degree Celsius

        Raises:
            Exception: When an error occurred on the device side
        """
        response: Response = await self._execute_command('ccd_getChipTemperature', {'index': self._id})
        return ureg.Quantity(response.results['temperature'], ureg.degC)  # type: ignore

    async def get_get_chip_size(self) -> Resolution:
        """Chip resolution of the CCD.

        Returns:
            Resolution: chip resolution (width, height)

        Raises:
            Exception: When an error occurred on the device side
        """
        response: Response = await self._execute_command('ccd_getChipSize', {'index': self._id})
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
        response: Response = await self._execute_command('ccd_getSpeed', {'index': self._id})
        return ureg(response.results['info'])

    async def get_exposure_time(self) -> Union[pint.Quantity, None]:
        """Returns the exposure time in ms

        Returns:
            pint.Quantity: Exposure time in ms
        Raises:
            Exception: When an error occurred on the device side
        """
        response: Response = await self._execute_command('ccd_getExposureTime', {'index': self._id})
        exposure = ureg.Quantity(response.results['time'], 'ms')
        return exposure

    async def set_exposure_time(self, exposure_time_ms: int) -> None:
        """Sets the exposure time in ms

        Args:
            exposure_time_ms (int): Exposure time in ms
        Raises:
            Exception: When an error occurred on the device side
        """

        await self._execute_command('ccd_setExposureTime',
                                    {'index': self._id, 'time': exposure_time_ms})

    async def get_acquisition_ready(self) -> bool:
        """Returns true if the CCD is ready to acquire

        Returns:
            bool: True if the CCD is ready to acquire
        Raises:
            Exception: When an error occurred on the device side
        """
        response: Response = await self._execute_command('ccd_getAcquisitionReady', {'index': self._id})
        return bool(response.results['size'])

    async def set_acquisition_start(self, open_shutter) -> None:
        """Starts the acquisition of the CCD
        Raises:
            Exception: When an error occurred on the device side
        """
        await self._execute_command('ccd_setAcquisitionStart', {'index': self._id, 'openShutter': open_shutter})

    async def set_region_of_interest(self, roi_index: int = 1, x_origin: int = 0, y_origin: int = 0, x_size: int = 1024,
                                     y_size: int = 256, x_bin: int = 1, y_bin: int = 256) -> None:
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
        await self._execute_command('ccd_setRoi',
                                    {'index': self._id, 'roiIndex': roi_index, 'xOrigin': x_origin,
                                     'yOrigin': y_origin, 'xSize': x_size, 'ySize': y_size, 'xBin': x_bin,
                                     'yBin': y_bin})

    async def get_acquisition_data(self) -> dict:
        """Returns the acquisition data of the CCD
        ToDo: atm this returns data still formatted for telnet communication, not formatted as json"""
        response: Response = await self._execute_command('ccd_getAcquisitionData', {'index': self._id})
        return response.results

    async def get_acquisition_busy(self) -> bool:
        """Returns true if the CCD is busy with the acquisition"""
        response: Response = await self._execute_command('ccd_getAcquisitionBusy', {'index': self._id})
        return bool(response.results['isBusy'])

    @staticmethod
    def _get_caller_name(self) -> str:
        # Get the current call stack
        stack: List[inspect.FrameInfo] = inspect.stack()
        # Check if the call stack has enough depth
        if len(stack) < 3:
            return 'Unknown'  # Not enough depth to have a caller
        # The caller is two frames up:
        # - index 0 is this function (stack) - index 1 is the function that called this function (get_caller_name)
        # - index 2 is the _execute_command caller - index 3 is the caller of _execute_command
        caller_frame: inspect.FrameInfo = stack[3]
        # Get the name of the caller function from the frame
        caller_name: str = caller_frame.function
        return caller_name

    def _handle_response_errors(self, response, param):
        if response.errors:
            self._device_manager.handle_errors(response.errors)
            raise Exception(f'{self._get_caller_name(self)} encountered error: {response.errors}')
