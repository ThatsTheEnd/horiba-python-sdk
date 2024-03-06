import asyncio
import os
import random

import pytest
from loguru import logger

from horiba_sdk.devices.device_manager import DeviceManager


# Tell pytest to run this test only if called from the scope of this module. If any other pytest scope calls this test,
# ignore it
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_functionality(event_loop):  # noqa: ARG001
    device_manager = DeviceManager()
    await device_manager.start()

    ccd = device_manager.charge_coupled_devices[0]
    await ccd.open()

    try:
        chip_size = await ccd.get_chip_size()
        assert chip_size.width > 0 and chip_size.height > 0
        await ccd.get_exposure_time()
        new_exposure_time = random.randint(1000, 5000)
        await ccd.set_exposure_time(new_exposure_time)
        assert await ccd.get_exposure_time() == new_exposure_time
        await ccd.get_temperature()
        await ccd.set_region_of_interest()  # Set default ROI, if you want a custom ROI, pass the parameters
        if await ccd.get_acquisition_ready():
            await ccd.set_acquisition_start(open_shutter=True)
            await asyncio.sleep(1)  # Wait a short period for the acquisition to start
            # Poll for acquisition status
            acquisition_busy = True
            while acquisition_busy:
                acquisition_busy = await ccd.get_acquisition_busy()
                await asyncio.sleep(0.3)
                logger.info('Acquisition busy')

            await ccd.get_acquisition_data()
        await ccd.get_speed()
    finally:
        await ccd.close()
        await device_manager.stop()
