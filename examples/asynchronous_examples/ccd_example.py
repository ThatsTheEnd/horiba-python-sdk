import asyncio
import random
import time

from loguru import logger
from horiba_sdk.devices.device_manager import DeviceManager
from horiba_sdk.devices.single_devices.ccd import ChargeCoupledDevice


async def binary_message_handler(message: bytes):
    # Process the binary message here
    logger.warning(f"Received binary message: {message}")


async def main():
    device_manager = DeviceManager(start_icl=False)
    # Register the binary message handler as the callback for incoming binary messages

    ccd = ChargeCoupledDevice(1, device_manager)
    await ccd.open()
    device_manager.communicator.register_binary_message_callback(binary_message_handler)

    try:
        await ccd.do_enable_binary_message()
        await ccd.get_get_chip_size()
        await ccd.get_exposure_time()
        await ccd.set_exposure_time(random.randint(1000, 5000))
        await ccd.get_exposure_time()
        await ccd.set_region_of_interest()  # Set default ROI
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
    finally:
        await ccd.close()


if __name__ == '__main__':
    asyncio.run(main())
