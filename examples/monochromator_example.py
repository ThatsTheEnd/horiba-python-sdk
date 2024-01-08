import asyncio

from horiba_sdk.devices.single_devices.monochromator import Monochromator
from horiba_sdk.devices.device_manager import DeviceManager


async def main():
    device_manager = DeviceManager()

    async with Monochromator(0, device_manager) as monochromator:
        print('Monochromator open? ' + str(await monochromator.is_open))


if __name__ == '__main__':
    asyncio.run(main())
