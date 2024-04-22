# pylint: skip-file
# Important note: the fake_icl_exe will return the contents of the
# horiba_sdk/devices/fake_responses/ccd.json
# Look at /test/conftest.py for the definition of fake_icl_exe

from horiba_sdk.core.gain import Gain
from horiba_sdk.core.speed import Speed


async def test_ccd_opens(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    # act
    async with fake_device_manager.charge_coupled_devices[0] as ccd:
        # assert
        assert await ccd.is_open() is True


async def test_ccd_temperature(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    # act
    async with fake_device_manager.charge_coupled_devices[0] as ccd:
        # assert
        temperature = await ccd.get_temperature()
        assert temperature < 0.0


async def test_ccd_resolution(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    # act
    async with fake_device_manager.charge_coupled_devices[0] as ccd:
        # assert
        resolution = await ccd.get_chip_size()
        assert resolution.width > 0 and resolution.height > 0


async def test_ccd_speed(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    async with fake_device_manager.charge_coupled_devices[0] as ccd:
        # act
        speed = await ccd.get_speed(Speed.SyncerityOE)

        # assert
        assert speed == Speed.SyncerityOE._45_KHZ
        assert speed != Speed.SynapsePlus._50_KHZ_HS


async def test_ccd_gain(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    async with fake_device_manager.charge_coupled_devices[0] as ccd:
        # act
        gain = await ccd.get_gain(Gain.SyncerityOE)

        # assert
        assert gain == Gain.SyncerityOE.HIGH_SENSITIVITY
        assert gain != Gain.SynapsePlus.ULTIMATE_SENSITIVITY
