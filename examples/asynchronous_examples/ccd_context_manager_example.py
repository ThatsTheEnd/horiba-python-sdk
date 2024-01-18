import asyncio

from horiba_sdk.devices.device_manager import DeviceManager
from horiba_sdk.devices.single_devices.ccd import ChargeCoupledDevice


async def main():
    device_manager = DeviceManager(start_icl=True)

    async with ChargeCoupledDevice(1, device_manager) as ccd:
        resolution = await ccd.resolution
        print(f'Resolution {resolution.width} x {resolution.height} pixels')
        print(f'Exposure time: {await ccd.get_exposure_time()}')
        await ccd.set_exposure_time(50000)
        print(f'Exposure time: {await ccd.get_exposure_time()}')
        await ccd.set_acquisition_start()


if __name__ == '__main__':
    asyncio.run(main())
