# pylint: skip-file
# Important note: the FakeDeviceManager will return the contents of the
# horiba_sdk/devices/fake_responses/monochromator.json


def test_monochromator_opens(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    monochromator = fake_sync_device_manager.monochromators[0]

    # act
    monochromator.open()

    # assert
    assert monochromator.is_open() is True

    monochromator.close()


def test_monochromator_busy(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    monochromator = fake_sync_device_manager.monochromators[0]

    # act
    monochromator.open()

    # assert
    assert monochromator.is_busy is False

    monochromator.close()


def test_monochromator_wavelength(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    monochromator = fake_sync_device_manager.monochromators[0]

    # act
    monochromator.open()

    # assert
    assert monochromator.wavelength > 0

    monochromator.close()


def test_monochromator_can_move_to_wavelength(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    monochromator = fake_sync_device_manager.monochromators[0]

    # act
    monochromator.open()
    monochromator.move_to_wavelength(350)

    # assert
    assert monochromator.wavelength > 0

    monochromator.close()


def test_monochromator_turret_grating_position(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    monochromator = fake_sync_device_manager.monochromators[0]

    # act
    monochromator.open()

    # assert
    assert monochromator.turret_grating_position > 0

    monochromator.close()


def test_monochromator_can_move_turret_grating_position(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    monochromator = fake_sync_device_manager.monochromators[0]

    # act
    monochromator.open()
    monochromator.move_turret_to_grating(50)

    # assert
    assert monochromator.turret_grating_position > 0

    monochromator.close()
