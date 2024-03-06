
from loguru import logger

from horiba_sdk.devices import EasyDeviceManager


def main():
    # Start the ICL to allow communication with the devices.
    device_manager = EasyDeviceManager(start_icl=True)
    device_manager.start()

    if not device_manager.charge_coupled_devices:
        logger.error('No CCDs found, exiting...')
        device_manager.stop()
        return
    logger.info(f'Found #{len(device_manager.charge_coupled_devices)}')

    ccd = device_manager.charge_coupled_devices[0]
    ccd.open()

    #device_manager.discover_devices()
    # print(f'CCD list: {device_manager.ccd_list}')
    # # ToDo: replace the hardcoded "1" in the next call with the first item of the list of discovered devices
    # # Get a CD object and open the connection to the CCD
    # ccd = EasyCCD(1, device_manager)
    # # Get and set some properties of the CCD
    # resolution = ccd.get_resolution()
    # print(f'Resolution {resolution.width} x {resolution.height} pixels')
    # print(f'Exposure time: {ccd.get_exposure_time()}')
    # ccd.set_exposure_time(5000)
    # print(f'Exposure time: {ccd.get_exposure_time()}')
    # ccd.set_acquisition_start(shutter_open=False)
    # data = ccd.get_acquisition_data()
    # print(f'Acquisition data: {data}')
    # # Close the CCD
    # ccd.close()
    device_manager.stop()


if __name__ == '__main__':
    main()
