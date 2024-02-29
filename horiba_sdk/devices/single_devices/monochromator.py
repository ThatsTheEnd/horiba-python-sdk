from enum import Enum
from types import TracebackType
from typing import Optional, final

from loguru import logger
from overrides import override

from horiba_sdk.communication import AbstractCommunicator, Response
from horiba_sdk.icl_error import AbstractErrorDB

from .abstract_device import AbstractDevice


@final
class Monochromator(AbstractDevice):
    """Monochromator device

    This class should not be instanced by the end user. Instead, the :class:`horiba_sdk.devices.DeviceManager`
    should be used to access the detected Monochromators on the system.
    """

    @final
    class ShutterStatus(Enum):
        CLOSED = 0
        OPEN = 1

    def __init__(self, device_id: int, communicator: AbstractCommunicator, error_db: AbstractErrorDB) -> None:
        super().__init__(device_id, communicator, error_db)

    async def __aenter__(self) -> 'Monochromator':
        await self.open()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException], exc_value: BaseException, traceback: Optional[TracebackType]
    ) -> None:
        is_open = await self.is_open()
        if not is_open:
            logger.debug('Monochromator is already closed')
            return

        await self.close()

    @override
    async def open(self) -> None:
        """Opens the connection to the Monochromator

        Raises:
            Exception: When an error occured on the device side
        """
        await super().open()
        await super()._execute_command('mono_open', {'index': self._id})

    @override
    async def close(self) -> None:
        """Closes the connection to the Monochromator

        Raises:
            Exception: When an error occured on the device side
        """
        await super()._execute_command('mono_close', {'index': self._id})

    async def is_open(self) -> bool:
        """Checks if the connection to the monochromator is open.

        Raises:
            Exception: When an error occured on the device side
        """
        response: Response = await super()._execute_command('mono_isOpen', {'index': self._id})
        return bool(response.results['open'])

    async def is_busy(self) -> bool:
        """Checks if the monochromator is busy.

        Raises:
            Exception: When an error occured on the device side
        """
        response: Response = await super()._execute_command('mono_isBusy', {'index': self._id})
        return bool(response.results['busy'])

    async def home(self) -> None:
        """Starts the monochromator initialization process called "homing".

        Use :func:`Monochromator.is_busy()` to know if the operation is still taking place.

        Raises:
            Exception: When an error occured on the device side
        """
        await super()._execute_command('mono_init', {'index': self._id})

    async def get_current_wavelength(self) -> float:
        """Current wavelength of the monochromator's position in nm.

        Returns:
            float: The current wavelength in nm

        Raises:
            Exception: When an error occurred on the device side
        """
        response = await super()._execute_command('mono_getPosition', {'index': self._id})
        return float(response.results['wavelength'])

    async def calibrate_wavelength(self, wavelength: float) -> None:
        """This command sets the wavelength value of the current grating position of the monochromator.

        .. warning:: This could potentially un-calibrate the monochromator and report an incorrect wavelength
                     compared to the actual output wavelength.

        Args:
            wavelength (float): wavelength in nm

        Raises:
            Exception: When an error occurred on the device side
        """
        await super()._execute_command('mono_setPosition', {'index': self._id, 'wavelength': wavelength})

    async def move_to_target_wavelength(self, wavelength: float) -> None:
        """Orders the monochromator to move to the requested wavelength.

        Use :func:`Monochromator.is_busy()` to know if the operation is still taking place.

        Args:
            wavelength (nm): wavelength

        Raises:
            Exception: When an error occurred on the device side
        """
        await super()._execute_command('mono_moveToPosition', {'index': self._id, 'wavelength': wavelength}, 60)

    async def get_turret_grating_position(self) -> int:
        """Grating turret position.

        Returns:
            int: current grating turret position

        Raises:
            Exception: When an error occured on the device side
        """
        response: Response = await super()._execute_command('mono_getGratingPosition', {'index': self._id})
        return int(response.results['position'])

    async def set_turret_grating_position(self, position: int) -> None:
        """Move turret to grating position

        .. todo:: Get more information about how it works and clarify veracity of returned data

        Args:
            position (int): new grating position

        Raises:
            Exception: When an error occured on the device side
        """
        await super()._execute_command('mono_moveGrating', {'index': self._id, 'position': position})

    async def get_mirror_position(self) -> int:
        """ Mirror position in ???

        .. todo:: Get more information about possible values and explain elements contained in monochromator at top
           of this class.

        Returns:
            int: current mirror position
        """
        response: Response = await super()._execute_command('mono_getMirrorPosition', {'index': self._id, 'type': 1})
        return int(response.results['position'])

    async def get_shutter_status(self) -> ShutterStatus:
        """ Shutter status

        Returns:
            ShutterStatus: OPEN or CLOSED
        """
        response: Response = await super()._execute_command('mono_getShutterStatus', {'index': self._id})
        return self.ShutterStatus(response.results['position'])
