from types import TracebackType
from typing import Optional, final

from loguru import logger
from overrides import override

from horiba_sdk.communication import Response
from horiba_sdk.icl_error import AbstractErrorDB
from horiba_sdk.sync.communication.abstract_communicator import AbstractCommunicator
from horiba_sdk.sync.devices.single_devices.abstract_device import AbstractDevice


@final
class Monochromator(AbstractDevice):
    """Monochromator device

    This class should not be instanced by the end user. Instead, the :class:`horiba_sdk.sync.devices.DeviceManager`
    should be used to access the detected Monochromators on the system.
    """

    def __init__(self, device_id: int, communicator: AbstractCommunicator, error_db: AbstractErrorDB) -> None:
        super().__init__(device_id, communicator, error_db)

    def __enter__(self) -> 'Monochromator':
        self.open()
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if not self.is_open():
            logger.debug('Monochromator is already closed')
            return

        self.close()

    @override
    def open(self) -> None:
        """Opens the connection to the Monochromator

        Raises:
            Exception: When an error occured on the device side
        """
        super().open()
        super()._execute_command('mono_open', {'index': self._id}, 0.5)

    @override
    def close(self) -> None:
        """Closes the connection to the Monochromator

        Raises:
            Exception: When an error occured on the device side
        """
        super()._execute_command('mono_close', {'index': self._id})

    def is_open(self) -> bool:
        """Checks if the connection to the monochromator is open.

        Raises:
            Exception: When an error occured on the device side
        """
        response: Response = super()._execute_command('mono_isOpen', {'index': self._id})
        return bool(response.results['open'])

    @property
    def is_busy(self) -> bool:
        """Checks if the monochromator is busy.

        Raises:
            Exception: When an error occured on the device side
        """
        response: Response = super()._execute_command('mono_isBusy', {'index': self._id})
        return bool(response.results['busy'])

    def home(self) -> None:
        """Starts the monochromator initialization process called "homing".

        Use :func:`Monochromator.is_busy()` to know if the operation is still taking place.

        Raises:
            Exception: When an error occured on the device side
        """
        super()._execute_command('mono_init', {'index': self._id})

    @property
    def wavelength(self) -> float:
        """Current wavelength of the monochromator's position in nm.

        Raises:
            Exception: When an error occured on the device side
        """
        response = super()._execute_command('mono_getPosition', {'index': self._id})
        return float(response.results['wavelength'])

    def set_current_wavelength(self, wavelength: int) -> None:
        """This command sets the wavelength value of the current grating position of the monochromator.

        .. warning:: This could potentially uncalibrate the monochromator and report an incorrect wavelength compared to
                     the actual output wavelength.

        Args:
            wavelength (nm): wavelength

        Raises:
            Exception: When an error occured on the device side
        """
        super()._execute_command('mono_setPosition', {'index': self._id, 'wavelength': wavelength})

    def move_to_wavelength(self, wavelength_nm: float) -> None:
        """Orders the monochromator to move to the requested wavelength.

        Use :func:`Monochromator.is_busy()` to know if the operation is still taking place.

        Args:
            wavelength_nm (float): wavelength

        Raises:
            Exception: When an error occured on the device side
        """
        super()._execute_command('mono_moveToPosition', {'index': self._id, 'wavelength': wavelength_nm})

    @property
    def turret_grating_position(self) -> int:
        """Grating turret position.

        Returns:
            int: current grating turret position

        Raises:
            Exception: When an error occured on the device side
        """
        response: Response = super()._execute_command('mono_getGratingPosition', {'index': self._id})
        return int(response.results['position'])

    def move_turret_to_grating(self, position: int) -> None:
        """Move turret to grating position

        .. todo:: Get more information about how it works and clarify veracity of returned data

        Args:
            position (int): new grating position

        Raises:
            Exception: When an error occured on the device side
        """
        super()._execute_command('mono_getPosition', {'index': self._id, 'position': position})
