from loguru import logger

from horiba_sdk.sync.devices import DeviceManager


def main():
    # Start the ICL to allow communication with the devices.
    device_manager = DeviceManager(start_icl=True)
    device_manager.start()

    print(f'CCDs: {len(device_manager.charge_coupled_devices)}')
    if device_manager.charge_coupled_devices.empty():
        logger.error('No CCDs discovered')
        device_manager.stop()
        return

    ccd = device_manager.charge_coupled_devices[0]
    ccd.open()

    resolution = ccd.get_resolution()
    print(f'Resolution {resolution.width} x {resolution.height} pixels')
    print(f'Exposure time: {ccd.get_exposure_time()}')
    ccd.set_exposure_time(5000)
    print(f'Exposure time: {ccd.get_exposure_time()}')
    ccd.set_acquisition_start(shutter_open=False)
    data = ccd.get_acquisition_data()
    print(f'Acquisition data: {data}')

    # Close the CCD
    ccd.close()

    device_manager.stop()


if __name__ == '__main__':
    main()
