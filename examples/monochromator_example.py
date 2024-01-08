import asyncio

from horiba_sdk.devices.monochromator import Monochromator
from horiba_sdk.devices.device_manager import DeviceManager


async def main():
    device_manager = DeviceManager()
    # using the context manager:
    with Monochromator(0, device_manager) as monochromator:
        print(await monochromator.is_open)


if __name__ == '__main__':
    asyncio.run(main())
