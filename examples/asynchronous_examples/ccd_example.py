import asyncio

from horiba_sdk.devices.device_manager import DeviceManager
from horiba_sdk.devices.single_devices.ccd import ChargeCoupledDevice


async def main():
    device_manager = DeviceManager(start_icl=True)

    ccd = ChargeCoupledDevice(1, device_manager)
    await ccd.open()

    try:
        resolution = await ccd.resolution
        print(f'Resolution {resolution.width} x {resolution.height} pixels')
        print(f'Exposure time: {await ccd.get_exposure_time()}')
        await ccd.set_exposure_time(50000)
        print(f'Exposure time: {await ccd.get_exposure_time()}')
        await ccd.set_acquisition_start()
    finally:
        await ccd.close()


if __name__ == '__main__':
    asyncio.run(main())
