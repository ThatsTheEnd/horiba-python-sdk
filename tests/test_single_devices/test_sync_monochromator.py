# pylint: skip-file
# Important note: the FakeDeviceManager will return the contents of the
# horiba_sdk/devices/fake_responses/monochromator.json


from horiba_sdk.sync.devices.single_devices import Monochromator


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
    # act
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # assert
        assert monochromator.is_busy() is False


def test_monochromator_config(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # act
        config = monochromator.configuration()
        # assert
        assert config
        assert config != ''


def test_monochromator_wavelength(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # assert
        assert monochromator.get_current_wavelength() > 0


def test_monochromator_can_move_to_wavelength(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # assert
        monochromator.move_to_target_wavelength(350)
        assert monochromator.get_current_wavelength() > 0


def test_monochromator_turret_grating_position(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # act
        # assert
        assert monochromator.get_turret_grating() == Monochromator.Grating.SECOND


def test_monochromator_can_select_turret_grating(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # act
        monochromator.set_turret_grating(Monochromator.Grating.SECOND)
        # assert
        assert monochromator.get_turret_grating() == Monochromator.Grating.SECOND


def test_monochromator_filter_wheel(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # act
        # assert
        assert (
            monochromator.get_filter_wheel_position(Monochromator.FilterWheel.FIRST)
            == Monochromator.FilterWheelPosition.RED
        )


def test_monochromator_change_filter_wheel_position(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # act
        monochromator.set_filter_wheel_position(Monochromator.FilterWheel.FIRST, Monochromator.FilterWheelPosition.RED)
        # assert
        assert (
            monochromator.get_filter_wheel_position(Monochromator.FilterWheel.FIRST)
            == Monochromator.FilterWheelPosition.RED
        )


def test_monochromator_mirror_position(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # act
        # assert
        assert monochromator.get_mirror_position(Monochromator.Mirror.ENTRANCE) == Monochromator.MirrorPosition.AXIAL


def test_monochromator_change_mirror_position(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # act
        monochromator.set_mirror_position(Monochromator.Mirror.ENTRANCE, Monochromator.MirrorPosition.AXIAL)
        # assert
        assert monochromator.get_mirror_position(Monochromator.Mirror.ENTRANCE) == Monochromator.MirrorPosition.AXIAL


def test_monochromator_get_slit_position(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # act
        # assert
        assert monochromator.get_slit_position_in_mm(Monochromator.Slit.A) >= 0


def test_monochromator_set_slit_position(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # act
        monochromator.set_slit_position(Monochromator.Slit.A, 0.0)
        # assert
        assert monochromator.get_slit_position_in_mm(Monochromator.Slit.A) == 0


def test_monochromator_get_slit_step_position(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # act
        # assert
        assert monochromator.get_slit_step_position(Monochromator.Slit.A) == 0


def test_monochromator_set_slit_step_position(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # act
        monochromator.set_slit_step_position(Monochromator.Slit.A, 0)
        # assert
        assert monochromator.get_slit_step_position(Monochromator.Slit.A) == 0


def test_monochromator_shutter_position(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
    # arrange
    with fake_sync_device_manager.monochromators[0] as monochromator:
        # act
        monochromator.close_shutter()
        # assert
        assert monochromator.get_shutter_position(Monochromator.Shutter.FIRST) == Monochromator.ShutterPosition.CLOSED
