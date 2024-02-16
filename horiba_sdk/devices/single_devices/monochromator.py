from types import TracebackType
from typing import Optional, final

from loguru import logger
from numericalunits import nm
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

    @property
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

    @property
    async def wavelength(self) -> nm:
        """Current wavelength of the monochromator's position in nm.

        Raises:
            Exception: When an error occured on the device side
        """
        response = await super()._execute_command('mono_getPosition', {'index': self._id})
        return float(response.results['wavelength']) * nm

    async def set_current_wavelength(self, wavelength: nm) -> None:
        """This command sets the wavelength value of the current grating position of the monochromator.

        .. warning:: This could potentially uncalibrate the monochromator and report an incorrect wavelength compared to
                     the actual output wavelength.

        Args:
            wavelength (nm): wavelength

        Raises:
            Exception: When an error occured on the device side
        """
        await super()._execute_command('mono_setPosition', {'index': self._id, 'wavelength': wavelength / nm})

    async def move_to_wavelength(self, wavelength: nm) -> None:
        """Orders the monochromator to move to the requested wavelength.

        Use :func:`Monochromator.is_busy()` to know if the operation is still taking place.

        Args:
            wavelength (nm): wavelength

        Raises:
            Exception: When an error occured on the device side
        """
        await super()._execute_command('mono_moveToPosition', {'index': self._id, 'wavelength': wavelength / nm})

    @property
    async def turret_grating_position(self) -> int:
        """Grating turret position.

        Returns:
            int: current grating turret position

        Raises:
            Exception: When an error occured on the device side
        """
        response: Response = await super()._execute_command('mono_getGratingPosition', {'index': self._id})
        return int(response.results['position'])

    async def move_turret_to_grating(self, position: int) -> None:
        """Move turret to grating position

        .. todo:: Get more information about how it works and clarify veracity of returned data

        Args:
            position (int): new grating position

        Raises:
            Exception: When an error occured on the device side
        """
        await super()._execute_command('mono_getPosition', {'index': self._id, 'position': position})
