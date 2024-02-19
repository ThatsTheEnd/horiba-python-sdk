# pylint: skip-file
# Important note: the fake_icl_exe will return the contents of the
# horiba_sdk/devices/fake_responses/ccd.json
# Look at /test/conftest.py for the definition of fake_icl_exe

from horiba_sdk import ureg
from horiba_sdk.devices import DeviceManager


async def test_ccd_opens(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    # act
    async with fake_device_manager.charge_coupled_devices[0] as ccd:
        # assert
        assert await ccd.is_open() is True


async def test_ccd_temperature_with_fak_device_manager_and_fake_icl_exe(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    # act
    async with fake_device_manager.charge_coupled_devices[0] as ccd:
        # assert
        temperature = await ccd.get_temperature()
        zero = ureg.Quantity(0, ureg.degC)
        assert temperature != zero

async def test_ccd_temperature_with_fake_icl_exe(fake_icl_exe, fake_icl_host_fixture, fake_icl_port_fixture):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager(start_icl=False, websocket_ip=fake_icl_host_fixture,
                                   websocket_port=fake_icl_port_fixture)
    await device_manager.start()
    # act
    async with device_manager.charge_coupled_devices[0] as ccd:
        # assert
        temperature = await ccd.get_temperature()
        zero = ureg.Quantity(0, ureg.degC)
        assert temperature != zero

    await device_manager.stop()

async def test_ccd_resolution(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    # act
    async with fake_device_manager.charge_coupled_devices[0] as ccd:
        # assert
        resolution = await ccd.get_chip_size()
        assert resolution.width > 0 and resolution.height > 0


async def test_ccd_speed(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    # act
    async with fake_device_manager.charge_coupled_devices[0] as ccd:
        # assert
        speed = await ccd.get_speed()
        zero = ureg.Quantity(0, ureg.kHz)
        assert speed != zero
