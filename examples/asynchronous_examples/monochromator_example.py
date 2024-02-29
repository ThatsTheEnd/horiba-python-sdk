import asyncio

from loguru import logger

from horiba_sdk.devices.device_manager import DeviceManager


async def main():
    device_manager = DeviceManager(start_icl=False)
    await device_manager.start()

    if not device_manager.monochromators:
        logger.error('No monochromators found, exiting...')
        await device_manager.stop()
        return

    mono = device_manager.monochromators[0]
    await mono.open()
    logger.warning(await mono.get_current_wavelength())
    await mono.move_to_target_wavelength(100)
    mono_is_busy = True
    while mono_is_busy:
        await asyncio.sleep(0.1)
        mono_is_busy = mono.is_busy()
    logger.warning(await mono.get_current_wavelength())

    await mono.close()


if __name__ == '__main__':
    asyncio.run(main())
