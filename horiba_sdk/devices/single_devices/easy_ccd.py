import asyncio

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
        self.ccd = ChargeCoupledDevice(device_id, device_manager)
        self._open()

    def _open(self):
        """
        Opens the connection to the ChargeCoupledDevice.

        Returns:
            None
        """
        return asyncio.run(self.ccd.open())

    def get_resolution(self):
        """
        Gets the resolution of the CCD.

        Returns:
            Resolution: The resolution of the CCD.
        """
        return asyncio.run(self.ccd.resolution)

    def get_exposure_time(self):
        """
        Gets the exposure time of the CCD.

        Returns:
            float: The exposure time of the CCD.
        """
        return asyncio.run(self.ccd.get_exposure_time())

    def set_exposure_time(self, time):
        """
        Sets the exposure time of the CCD.

        Args:
            time (float): The exposure time to set.

        Returns:
            None
        """
        return asyncio.run(self.ccd.set_exposure_time(time))

    def set_acquisition_start(self):
        """
        Starts the acquisition of the CCD.

        Returns:
            None
        """
        return asyncio.run(self.ccd.set_acquisition_start())

    def close(self):
        """
        Closes the CCD.

        Returns:
            None
        """
        return asyncio.run(self.ccd.close())
