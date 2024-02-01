import asyncio
import time

from loguru import logger

from horiba_sdk.devices.device_manager import DeviceManager
from horiba_sdk.devices.single_devices.ccd import ChargeCoupledDevice


async def main():
    device_manager = DeviceManager(start_icl=False)

    async with ChargeCoupledDevice(1, device_manager) as ccd:
        try:
            resolution = await ccd.get_resolution()
            logger.info(f'Resolution: {resolution}')
            await ccd.get_exposure_time()
            await ccd.set_exposure_time(5000)
            await ccd.set_acquisition_start()
            time.sleep(6)
        except Exception as e:
            logger.error(e)

    logger.debug('Stopping ICL software...')
    await device_manager.stop_icl()
    time.sleep(2)
    logger.debug('ICL software stopped.')


if __name__ == '__main__':
    asyncio.run(main())