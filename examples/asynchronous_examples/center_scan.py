# Dependencies: matplotlib package
import asyncio

import matplotlib.pyplot as plt
from loguru import logger

from horiba_sdk.devices.device_manager import DeviceManager
import csv


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

        
        #await mono.set_mirror_position(mono.Mirror.FIRST, mono.MirrorPosition.A)
        #await wait_for_mono(mono)
        #await mono.set_slit_position(mono.Slit.A, 0.1)
        #await wait_for_mono(mono)
        await mono.set_turret_grating(mono.Grating.THIRD)
        await wait_for_mono(mono)
        target_wavelength = 1200
        await mono.move_to_target_wavelength(target_wavelength)
        await wait_for_mono(mono)
        mono_wavelength = await mono.get_current_wavelength()


        # ccd configuration
        await ccd.set_acquisition_count(1)
        await ccd.set_x_axis_conversion_type(ccd.XAxisConversionType(2))
        await ccd.set_exposure_time(500)
        await ccd.set_gain(ccd.Gain.HIGH_LIGHT)
        await ccd.set_speed(ccd.Speed.FAST_1_MHz_Ultra)
        await ccd.set_region_of_interest()  # Set default ROI, if you want a custom ROI, pass the parameters
        xy_data_str = '[[0,0]]'
        await ccd.set_center_wavelength(mono_wavelength)

        if await ccd.get_acquisition_ready():
            await ccd.set_acquisition_start(open_shutter=True)
            await asyncio.sleep(15)  # Wait a short period for the acquisition to start
            await wait_for_ccd(ccd)
                  

            raw_data = await ccd.get_acquisition_data()
            #print(type(raw_data))
            #print(type(raw_data['acquisition']))
            #for i in raw_data['acquisition']:
            #    print(i)
            # json data is invalid, we cannot do this:
            # json_data = json.loads(raw_data['data'])
            # center_scan_data = json_data['xyData']

            # Extracting xyData the hard way

            start_index = str(raw_data['acquisition']).find("'xyData': [")
            end_index = str(raw_data['acquisition']).find(']]', start_index) + 1
            xy_data_str = str(raw_data['acquisition'])[start_index + 10 : end_index + 1]
            with open('log.txt', 'w') as log:
                log.write(str(raw_data))
                log.write('\n')
                log.write(str(xy_data_str))
            log.close()

            #print(eval(xy_data_str))
            #print(type(eval(xy_data_str)))

            cleaner_data = eval(xy_data_str)

            with open('outputcsv.csv', 'w', newline = "") as csvfile:
                w = csv.writer(csvfile)
                fields = ['wavelength', 'intensity']
                w.writerow(fields)
                w.writerows(cleaner_data)
        

            
            #print(mono_wavelength)
            #print(type(mono_wavelength))
        

    finally:
        await ccd.close()
        logger.info('Waiting before closing Monochromator')
        await asyncio.sleep(1)
        await mono.close()

    await device_manager.stop()
    await plot_values(xy_data_str)


async def plot_values(xy_data_str):
    center_scan_data = eval(xy_data_str)
    x_values = [point[0] for point in center_scan_data]
    y_values = [point[1] for point in center_scan_data]
    # Plotting the data
    plt.plot(x_values, y_values, linestyle='-')
    plt.title(f'Wavelength vs. Intensity')
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