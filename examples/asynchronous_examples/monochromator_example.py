import asyncio

from horiba_sdk.devices.device_manager import DeviceManager
from horiba_sdk.devices.single_devices.monochromator import Monochromator


async def main():
    device_manager = DeviceManager()
    await device_manager.communicator.open()
    await device_manager.discover_devices()

    mono = Monochromator(device_manager)
    await mono.open(0)
    print('Monochromator open? ' + str(await mono.is_open))
    await mono.close()

    await device_manager.stop_icl()


if __name__ == '__main__':
    asyncio.run(main())
