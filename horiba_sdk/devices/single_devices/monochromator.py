import time
import logging
from typing import Tuple, Union, List, TYPE_CHECKING
from horiba_sdk.devices.device_manager import DeviceManager
from horiba_sdk.devices.single_devices.abstract_device import AbstractDevice

if TYPE_CHECKING:
    from horiba_sdk.communication import AbstractCommunicator


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Monochromator(AbstractDevice):
    """API for controlling and querying the monochromator using the Telnet interface."""

    def __init__(
        self,
        mono_number: int,
        device_manager: DeviceManager,
    ) -> None:
        """
        Initialize the MonoApi instance.

        Args:
            mono_number (int): The integer number for the mono that is to be controlled.

        Raises:
            ValueError: If the communicator instance is None.
        """
        self._mono_number = mono_number
        self._communicator = device_manager.communicator
        if self._communicator is None:
            raise ValueError("Communicator cannot be None")
        super().__init__(device_manager)

    def _run_command(
        self,
        command: str,
        value: Union[int, None] = None,
        parameter: Union[str, None] = None,
    ) -> Union[str, List[str]]:
        """
        Run the Telnet command and check the response.

        Args:
            command (str): Command to be executed.
            value (Union[int, None]): Optional value to pass with command. Default to None.
            parameter (Union[int, None]): can be a third argument, e.g. when setting the wavelength

        Raises:
            RuntimeError: If there's a communication error with Telnet.

        Returns:
            List[str]: Response from Telnet.
        """
        if parameter:
            response = self._communicator.send_and_receive(
                f"{command} {self._mono_number} {value} {parameter}"
            )
        elif value:
            response = self._communicator.send_and_receive(
                f"{command} {self._mono_number} {value}"
            )
        else:
            response = self._communicator.send_and_receive(
                f"{command} {self._mono_number}"
            )

        # Assuming that a negative response code (rc) indicates an error.
        # You might need to adjust this depending on the actual responses you receive.
        if response[0].startswith("-"):
            raise RuntimeError(f"Telnet Communications error! Response: {response[0]}")

        return response

    def open(self) -> None:
        """Open and home the monochromator. This function is implemented to adhere to abc device

        :return:
        """
        self.home()

    def home(self) -> None:
        """Initialize and home the monochromator.

        Args:
        """
        self._run_command("lmb_monoInit", self._mono_number)
        logger.info("Homing mono")
        while self.is_mono_busy():
            logger.info("Mono busy")
            time.sleep(0.5)
        logger.info("Mono homed")

    def wavelength_limits(self) -> Tuple[str, str]:
        """Retrieve the wavelength limits of the monochromator.

        Returns:
            Tuple[str, str]: Minimum and maximum wavelength limits.
        """
        response = self._run_command("lmb_monoWaveLim", self._mono_number)
        return response[0].strip(), response[1].strip()

    def set_wavelength(self, wavelength: int) -> None:
        """Set the monochromator to a specific wavelength without waiting.

        Args:
            wavelength (int): Desired wavelength.
        """
        self._run_command("lmb_monoSetWave", self._mono_number, str(wavelength))

    def move_to_no_wait(self, wavelength: int) -> None:
        """
        Move the monochromator to a specific wavelength and return immediately without waiting for the operation to
        complete.

        Args:
            wavelength (int): Desired wavelength.
        """
        while self.is_mono_busy():
            logger.info("Mono position: %s", self.mono_current_position())
            time.sleep(0.5)
        self._run_command("lmb_monoMoveTo", self._mono_number, str(wavelength))

    def move_to(self, wavelength: int) -> None:
        """
        Move the monochromator to a specific wavelength and wait for the operation to complete.

        Args:
            wavelength (int): Desired wavelength.
        """
        self._run_command("lmb_monoMoveTo", self._mono_number, str(wavelength))
        while self.is_mono_busy():
            time.sleep(0.5)
        logger.info("Mono position: %s", self.mono_current_position())

    def is_mono_busy(self) -> bool:
        """
        Check if the monochromator is busy.

        Returns:
            bool: True if the monochromator is busy, otherwise False.
        """
        response = self._run_command("lmb_monoBusy", self._mono_number)
        return response[0].startswith("1")

    def stop(self) -> bool:
        """Stop the current operation of the monochromator.

        Returns:
            bool: True if the stop command was successful, otherwise False.
        """
        response = self._run_command("lmb_monoStop", self._mono_number)
        return response[0].startswith("1")

    def mono_current_position(self) -> str:
        """Retrieve the current position of the monochromator.

        Returns:
            str: Current position of the monochromator.
        """
        response = self._run_command("lmb_monoPosition", self._mono_number)
        return response[0].strip()

    def mono_status(self) -> str:
        """Retrieve the status of the monochromator.

        Returns:
            str: Status of the monochromator.
        """
        response = self._run_command("lmb_monoStatus", self._mono_number)
        return response[0].strip()

    def set_wave(self, wavelength: int) -> None:
        """Set the monochromator to a specific wavelength and wait for the operation to complete.

        Args:
            wavelength (int): Desired wavelength.
        """
        logger.info("Mono position: %s", self.mono_current_position())
        self._run_command("lmb_monoSetWave", self._mono_number, str(wavelength))
        while self.is_mono_busy():
            logger.info("Mono position: %s", self.mono_current_position())
            time.sleep(0.5)
        logger.info("Mono position: %s", self.mono_current_position())

    def get_grating_info(self) -> str:
        """Retrieve information about the monochromator's grating.

        Returns:
            str: Grating information.
        """
        response = self._run_command("lmb_monoGrateInfo")
        logger.info(response)
        return response[0].strip()

    def close(self) -> None:
        """Add any code to close device

        :return:
        """
