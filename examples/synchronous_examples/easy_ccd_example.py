from horiba_sdk.devices.device_manager import DeviceManager
from horiba_sdk.devices.single_devices.easy_ccd import EasyCCD


async def main():
    # Start the ICL to allow communication with the devices.
    device_manager: DeviceManager = DeviceManager(start_icl=False)
    # nina wrap the device manager class into an easy device manager without async calls
    device_manager.discover_devices()
    print(f'CCD list: {device_manager.ccd_list}')
    # ToDo: replace the hardcoded "1" in the next call with the first item of the list of discovered devices
    # Get a CD object and open the connection to the CCD
    ccd = EasyCCD(1, device_manager)
    # Get and set some properties of the CCD
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
    device_manager.stop_icl()


if __name__ == '__main__':
    main()
