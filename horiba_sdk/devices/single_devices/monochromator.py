from types import TracebackType
from typing import Optional, final

from numericalunits import nm
from overrides import override

from horiba_sdk.communication.messages import Command, Response
from horiba_sdk.devices.abstract_device_manager import AbstractDeviceManager

from .abstract_device import AbstractDevice


@final
class Monochromator(AbstractDevice):
    """Monochromator device

    Example usage::

        from horiba_sdk.devices.monochromator import Monochromator

        # using the context manager:
        with Monochromator(0, device_manager) as monochromator:
            print(await monochromator.is_open)

        # alternative usage
        monochromator: Monochromator = Monochromator(0, device_manager)
        await monochromator.open()
        print(await monochromator.is_open)
        await monochromator.close()


    .. todo:: Handle errors coming from the ICL. There may be more than one, in the format:
       `"[E];<error code>;<error string>"`

    """

    def __init__(self, id: int, device_manager: AbstractDeviceManager) -> None:
        super().__init__(id, device_manager)

    async def __aenter__(self) -> 'Monochromator':
        await self.open()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException], exc_value: BaseException, traceback: Optional[TracebackType]
    ) -> None:
        await self.close()

    @override
    async def open(self) -> None:
        """Opens the connection to the Monochromator

        Raises:
            Exception: When an error occured on the device side
        """
        await super().open()
        command = Command('mono_open', {'index': self._id})
        await self._communicator.send(command)
        _ignored_response = await self._communicator.response()

        if _ignored_response.errors:
            raise Exception(f'Monochromator encountered error: {_ignored_response.errors}')

    @override
    async def close(self) -> None:
        """Closes the connection to the Monochromator

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('mono_close', {'index': self._id})
        await self._communicator.send(command)
        _ignored_response = await self._communicator.response()
        await super().close()

        if _ignored_response.errors:
            raise Exception(f'Monochromator encountered error: {_ignored_response.errors}')

    @property
    async def is_open(self) -> bool:
        """Checks if the connection to the monochromator is open.

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('mono_isOpen', {'index': self._id})
        await self._communicator.send(command)
        response: Response = await self._communicator.response()
        if response.errors:
            raise Exception(f'Monochromator encountered error: {response.errors}')

        return bool(response.results['open'])

    @property
    async def is_busy(self) -> bool:
        """Checks if the monochromator is busy.

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('mono_isBusy', {'index': self._id})
        await self._communicator.send(command)
        response: Response = await self._communicator.response()
        if response.errors:
            raise Exception(f'Monochromator encountered error: {response.errors}')

        return bool(response.results['busy'])

    async def home(self) -> None:
        """Starts the monochromator initialization process called "homing".

        Use :func:`Monochromator.is_busy()` to know if the operation is still taking place.

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('mono_init', {'index': self._id})
        await self._communicator.send(command)
        _ignored_response = await self._communicator.response()

        if _ignored_response.errors:
            raise Exception(f'Monochromator encountered error: {_ignored_response.errors}')

    @property
    async def wavelength(self) -> nm:
        """Current wavelength of the monochromator's position in nm.

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('mono_getPosition', {'index': self._id})
        await self._communicator.send(command)
        response: Response = await self._communicator.response()
        if response.errors:
            raise Exception(f'Monochromator encountered error: {response.errors}')

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
        command = Command('mono_setPosition', {'index': self._id, 'wavelength': wavelength / nm})
        await self._communicator.send(command)
        _ignored_response = await self._communicator.response()

        if _ignored_response.errors:
            raise Exception(f'Monochromator encountered error: {_ignored_response.errors}')

    async def move_to_wavelength(self, wavelength: nm) -> None:
        """Orders the monochromator to move to the requested wavelength.

        Use :func:`Monochromator.is_busy()` to know if the operation is still taking place.

        Args:
            wavelength (nm): wavelength

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('mono_moveToPosition', {'index': self._id, 'wavelength': wavelength / nm})
        await self._communicator.send(command)
        _ignored_response = await self._communicator.response()

        if _ignored_response.errors:
            raise Exception(f'Monochromator encountered error: {_ignored_response.errors}')

    @property
    async def turret_grating_position(self) -> int:
        """Grating turret position.

        Returns:
            int: current grating turret position

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('mono_getGratingPosition', {'index': self._id})
        await self._communicator.send(command)
        response: Response = await self._communicator.response()
        if response.errors:
            raise Exception(f'Monochromator encountered error: {response.errors}')

        return int(response.results['position'])

    async def move_turret_to_grating(self, position: int) -> None:
        """Move turret to grating position

        .. todo:: Get more information about how it works and clarify veracity of returned data

        Args:
            position (int): new grating position

        Raises:
            Exception: When an error occured on the device side
        """
        command = Command('mono_getPosition', {'index': self._id, 'position': position})
        await self._communicator.send(command)
        _ignored_response = await self._communicator.response()

        if _ignored_response.errors:
            raise Exception(f'Monochromator encountered error: {_ignored_response.errors}')
