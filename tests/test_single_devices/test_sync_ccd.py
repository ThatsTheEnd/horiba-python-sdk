# pylint: skip-file
# Important note: the fake_icl_exe will return the contents of the
# horiba_sdk/devices/fake_responses/ccd.json
# Look at /test/conftest.py for the definition of fake_icl_exe

from horiba_sdk import ureg


def test_ccd_opens(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    # act
    with fake_sync_device_manager.charge_coupled_devices[0] as ccd:
        # assert
        assert ccd.is_open() is True


def test_ccd_temperature(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    # act
    with fake_sync_device_manager.charge_coupled_devices[0] as ccd:
        # assert
        temperature = ccd.get_temperature()
        zero = ureg.Quantity(0, ureg.degC)
        assert temperature != zero


def test_ccd_resolution(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    # act
    with fake_sync_device_manager.charge_coupled_devices[0] as ccd:
        # assert
        resolution = ccd.get_chip_size()
        assert resolution.width > 0 and resolution.height > 0


def test_ccd_speed(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    # act
    with fake_sync_device_manager.charge_coupled_devices[0] as ccd:
        # assert
        speed = ccd.get_speed()
        zero = ureg.Quantity(0, ureg.kHz)
        assert speed != zero
