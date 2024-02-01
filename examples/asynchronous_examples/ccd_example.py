import asyncio
import random
import time

from loguru import logger
from horiba_sdk.devices.device_manager import DeviceManager
from horiba_sdk.devices.single_devices.ccd import ChargeCoupledDevice


async def main():
    device_manager = DeviceManager(start_icl=False)
    await device_manager.communicator.open()
    await device_manager.discover_devices()

    ccd = ChargeCoupledDevice(device_manager)
    await ccd.open(1)

    try:
        await ccd.do_enable_binary_message()
        await ccd.get_get_chip_size()
        await ccd.get_exposure_time()
        await ccd.set_exposure_time(random.randint(1000, 5000))
        await ccd.get_exposure_time()
        await ccd.get_temperature()
        await ccd.set_region_of_interest()  # Set default ROI, if you want a custom ROI, pass the parameters
        if await ccd.get_acquisition_ready():
            await ccd.set_acquisition_start(open_shutter=False)
            time.sleep(1)  # Wait a short period for the acquisition to start
            # Poll for acquisition status
            acquisition_busy = True
            while acquisition_busy:
                acquisition_busy = await ccd.get_acquisition_busy()
                await asyncio.sleep(0.3)
                logger.info("Acquisition busy")

            await ccd.get_acquisition_data()
        await ccd.get_speed()
    finally:
        await ccd.close()


if __name__ == '__main__':
    asyncio.run(main())
