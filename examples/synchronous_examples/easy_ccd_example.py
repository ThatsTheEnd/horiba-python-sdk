from horiba_sdk.devices.device_manager import DeviceManager
from horiba_sdk.devices.single_devices.easy_ccd import EasyCCD


def main():
    # Start the ICL to allow communication with the devices.
    device_manager = DeviceManager(start_icl=True)
    # ToDo: Implement discover to find all devices (monos and ccds atm) and save them internally
    device_manager.discover()
    # ToDo: replace the hardcoded "1" in the next call with the first item of the list of discovered devices
    # Get a CD object and open the conenction to the CCD
    ccd = EasyCCD(1, device_manager)

    # Get and set some properties of the CCD
    resolution = ccd.get_resolution()
    print(f'Resolution {resolution.width} x {resolution.height} pixels')
    print(f'Exposure time: {ccd.get_exposure_time()}')
    ccd.set_exposure_time(50000)
    print(f'Exposure time: {ccd.get_exposure_time()}')
    ccd.set_acquisition_start()
    # ToDo: Implement a way to fetch the data from the CCD

    # Close the CCD
    ccd.close()
    device_manager.stop_icl()


if __name__ == '__main__':
    main()
