from loguru import logger

from horiba_sdk.sync.devices.device_manager import DeviceManager


def main():
    device_manager = DeviceManager()
    device_manager.start()

    print(f'Monochromators: {len(device_manager.monochromators)}')
    if len(device_manager.monochromators) == 0:
        logger.error('No Monochromators discovered')
        device_manager.stop()
        return

    with device_manager.monochromators[0] as mono:
        print('Monochromator open? ' + str(mono.is_open))

    device_manager.stop()


if __name__ == '__main__':
    main()
