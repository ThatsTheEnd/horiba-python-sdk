import asyncio
from typing import Any

from .ccd import ChargeCoupledDevice


class EasyCCD:
    """
    This class provides a synchronous interface to the ChargeCoupledDevice class.
    It was created to allow users who are not familiar with asynchronous programming
    to use the ChargeCoupledDevice class in a synchronous manner.

    Each method in this class wraps a corresponding method in the ChargeCoupledDevice
    class with asyncio.run(), which runs the method in a blocking manner.

    Note: This class should be used in scripts or applications that are not already
    running an event loop. If an event loop is already running, the asyncio.run()
    calls will raise an error.

    Args:
        device_id (int): The ID of the device.
        device_manager (DeviceManager): The device manager instance.
    """

    def __init__(self, device_id, device_manager):
        """
        Initializes a new instance of the EasyCCD class.
        The main difference between this class and the ChargeCoupledDevice class is that
        this class provides a synchronous interface to the ChargeCoupledDevice class.
        It was created to allow users who are not familiar with asynchronous programming
        to use the ChargeCoupledDevice class in a synchronous manner.

        Args:
            device_id (int): The ID of the device.
            device_manager (DeviceManager): The device manager instance.
        """
        self.ccd = ChargeCoupledDevice(device_manager)
        self._open(device_id)

    def _open(self, device_id):
        """
        Opens the connection to the ChargeCoupledDevice.

        Returns:
            None
        """
        return asyncio.run(self.ccd.open(device_id))

    def get_resolution(self):
        """
        Gets the resolution of the CCD.

        Returns:
            Resolution: The resolution of the CCD.
        """
        return asyncio.run(self.ccd.get_get_chip_size())

    def get_exposure_time(self):
        """
        Gets the exposure time of the CCD.

        Returns:
            float: The exposure time of the CCD.
        """
        return asyncio.run(self.ccd.get_exposure_time())

    def set_exposure_time(self, exposure_time_ms):
        """
        Sets the exposure time [ms] of the CCD.

        Args:
            exposure_time_ms (int): The exposure time in [ms] to set.

        Returns:
            None
        """
        return asyncio.run(self.ccd.set_exposure_time(exposure_time_ms))

    def set_acquisition_start(self, shutter_open):
        """
        Starts the acquisition of the CCD.

        Returns:
            None
        """
        return asyncio.run(self.ccd.set_acquisition_start(shutter_open))

    def get_acquisition_data(self) -> dict[Any, Any]:
        """
        Gets the acquisition data from the CCD.

        Returns:
            dict: The acquisition data from the CCD.
        """
        return asyncio.run(self.ccd.get_acquisition_data())

    def close(self):
        """
        Closes the CCD.

        Returns:
            None
        """
        return asyncio.run(self.ccd.close())
