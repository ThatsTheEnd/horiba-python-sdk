# Dependencies: matplotlib package
import asyncio

import matplotlib.pyplot as plt
from loguru import logger

from horiba_sdk.core.acquisition_format import AcquisitionFormat
from horiba_sdk.core.x_axis_conversion_type import XAxisConversionType
from horiba_sdk.devices.device_manager import DeviceManager


async def main():
    device_manager = DeviceManager(start_icl=True)
    await device_manager.start()

    if not device_manager.charge_coupled_devices or not device_manager.monochromators:
        logger.error('Required monochromator or ccd not found')
        await device_manager.stop()
        return

    mono = device_manager.monochromators[0]
    await mono.open()
    await wait_for_mono(mono)
    ccd = device_manager.charge_coupled_devices[0]
    await ccd.open()
    await wait_for_ccd(ccd)

    try:
        # mono configuration
        await mono.home()
        await wait_for_mono(mono)

        target_wavelength = 100.0
        await mono.move_to_target_wavelength(target_wavelength)
        await wait_for_mono(mono)

        # ccd configuration
        await ccd.set_acquisition_format(1, AcquisitionFormat.IMAGE)
        await ccd.set_acquisition_count(1)
        await ccd.set_x_axis_conversion_type(XAxisConversionType.NONE)
        await ccd.set_exposure_time(1000)
        await ccd.set_region_of_interest()  # Set default ROI, if you want a custom ROI, pass the parameters
        xy_data = [[0], [0]]

        if await ccd.get_acquisition_ready():
            await ccd.set_acquisition_start(open_shutter=True)
            await asyncio.sleep(1)  # Wait a short period for the acquisition to start
            await wait_for_ccd(ccd)

            raw_data = await ccd.get_acquisition_data()
            print(raw_data)
            xy_data = [raw_data[0]['roi'][0]['xData'][0], raw_data[0]['roi'][0]['yData'][0]]
    finally:
        await ccd.close()
        logger.info('Waiting before closing Monochromator')
        await asyncio.sleep(15)
        await mono.close()

    await device_manager.stop()

    await plot_values(target_wavelength, xy_data)


async def plot_values(target_wavelength, xy_data):
    x_values = xy_data[0]
    y_values = xy_data[1]
    # Plotting the data
    plt.plot(x_values, y_values, linestyle='-')
    plt.title(f'Wavelength ({target_wavelength}[nm]) vs. Intensity')
    plt.xlabel('Wavelength')
    plt.ylabel('Intensity')
    plt.grid(True)
    plt.show()


async def wait_for_ccd(ccd):
    acquisition_busy = True
    while acquisition_busy:
        acquisition_busy = await ccd.get_acquisition_busy()
        await asyncio.sleep(0.3)
        logger.info('Acquisition busy')


async def wait_for_mono(mono):
    mono_busy = True
    while mono_busy:
        mono_busy = await mono.is_busy()
        await asyncio.sleep(1)
        logger.info('Mono busy...')


if __name__ == '__main__':
    asyncio.run(main())
