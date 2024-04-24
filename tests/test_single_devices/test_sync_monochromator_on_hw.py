# pylint: skip-file

import os
import time

import pytest

from horiba_sdk.sync.devices import DeviceManager
from horiba_sdk.sync.devices.single_devices import Monochromator


@pytest.fixture(scope='module')
def device_manager_instance():
    device_manager = DeviceManager(start_icl=True)

    device_manager.start()

    yield device_manager

    device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_opens(device_manager_instance):
    # arrange
    # act
    with device_manager_instance.monochromators[0] as monochromator:
        # assert
        assert monochromator.is_open() is True


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_busy(device_manager_instance):
    # arrange
    with device_manager_instance.monochromators[0] as monochromator:
        # act
        # assert
        assert monochromator.is_busy() is False


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_init(device_manager_instance):
    # arrange
    with device_manager_instance.monochromators[0] as monochromator:
        # act
        monochromator.home()

        while monochromator.is_busy():
            time.sleep(1)

        # assert
        assert monochromator.is_busy() is False


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_config(device_manager_instance):  # noqa: ARG001
    # arrange
    with device_manager_instance.monochromators[0] as monochromator:
        # act
        config = monochromator.configuration()

        # assert
        assert config
        assert config != ''


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_wavelength(device_manager_instance):
    # arrange
    with device_manager_instance.monochromators[0] as monochromator:
        # act
        monochromator.move_to_target_wavelength(100)

        while monochromator.is_busy():
            time.sleep(1)

        # assert
        assert monochromator.get_current_wavelength() > 0


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_calibrate_wavelength(device_manager_instance):
    # arrange
    with device_manager_instance.monochromators[0] as monochromator:
        # act
        # TODO: How to test this properly???
        # monochromator.calibrate_wavelength(350)

        # assert
        # assert monochromator.get_current_wavelength() > 0
        assert not monochromator.is_busy()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_turret_grating_position(device_manager_instance):
    # arrange
    with device_manager_instance.monochromators[0] as monochromator:
        expected_grating = Monochromator.Grating.FIRST

        # act
        monochromator.set_turret_grating(expected_grating)

        while monochromator.is_busy():
            time.sleep(1)

        actual_grating = monochromator.get_turret_grating()

        # assert
        assert actual_grating == expected_grating


# Note: Filter wheel not available on our mono
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_filter_wheel(device_manager_instance):  # noqa: ARG001
    # arrange
    with device_manager_instance.monochromators[0] as monochromator:
        filter_wheel = Monochromator.FilterWheel.SECOND
        expected_filter_wheel_position_before = Monochromator.FilterWheelPosition.RED
        expected_filter_wheel_position_after = Monochromator.FilterWheelPosition.GREEN

        # act
        monochromator.set_filter_wheel_position(filter_wheel, expected_filter_wheel_position_before)
        while monochromator.is_busy():
            time.sleep(1)
        actual_filter_wheel_position_before = monochromator.get_filter_wheel_position(filter_wheel)

        monochromator.set_filter_wheel_position(filter_wheel, expected_filter_wheel_position_after)
        while monochromator.is_busy():
            time.sleep(1)
        actual_filter_wheel_position_after = monochromator.get_filter_wheel_position(filter_wheel)

        # assert
        assert actual_filter_wheel_position_before == expected_filter_wheel_position_before
        assert actual_filter_wheel_position_after == expected_filter_wheel_position_after


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_mirror(device_manager_instance):  # noqa: ARG001
    # arrange
    with device_manager_instance.monochromators[0] as monochromator:
        expected_mirror_position_before = Monochromator.MirrorPosition.LATERAL
        expected_mirror_position_after = Monochromator.MirrorPosition.AXIAL

        # act
        monochromator.set_mirror_position(Monochromator.Mirror.FIRST, expected_mirror_position_before)
        while monochromator.is_busy():
            time.sleep(1)

        actual_mirror_position_before = monochromator.get_mirror_position(Monochromator.Mirror.FIRST)

        monochromator.set_mirror_position(Monochromator.Mirror.FIRST, expected_mirror_position_after)
        while monochromator.is_busy():
            time.sleep(1)

        actual_mirror_position_after = monochromator.get_mirror_position(Monochromator.Mirror.FIRST)

        # assert
        assert actual_mirror_position_before == expected_mirror_position_before
        assert actual_mirror_position_after == expected_mirror_position_after


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_slit(device_manager_instance):  # noqa: ARG001
    # arrange
    with device_manager_instance.monochromators[0] as monochromator:
        monochromator.home()
        while monochromator.is_busy():
            time.sleep(1)

        expected_slit_position_mm_before = 1.5
        expected_slit_position_mm_after = 2.6
        slit = Monochromator.Slit.A

        # act
        monochromator.set_slit_position(slit, expected_slit_position_mm_before)
        while monochromator.is_busy():
            time.sleep(1)

        actual_slit_position_mm_before = monochromator.get_slit_position_in_mm(slit)

        monochromator.set_slit_position(slit, expected_slit_position_mm_after)
        while monochromator.is_busy():
            time.sleep(1)

        actual_slit_position_mm_after = monochromator.get_slit_position_in_mm(slit)

        # assert
        assert (actual_slit_position_mm_before - expected_slit_position_mm_before) < 10e-9
        assert (actual_slit_position_mm_after - expected_slit_position_mm_after) < 10e-9


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_shutter(device_manager_instance):
    # arrange
    with device_manager_instance.monochromators[0] as monochromator:
        expected_shutter_position_before = Monochromator.ShutterPosition.CLOSED
        expected_shutter_position_after = Monochromator.ShutterPosition.OPENED

        # act
        monochromator.close_shutter()
        actual_shutter_status_before = monochromator.get_shutter_position(Monochromator.Shutter.FIRST)

        monochromator.open_shutter()
        actual_shutter_status_after = monochromator.get_shutter_position(Monochromator.Shutter.FIRST)

        # assert
        assert actual_shutter_status_before == expected_shutter_position_before
        assert actual_shutter_status_after == expected_shutter_position_after


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_slit_step_position(device_manager_instance):  # noqa: ARG001
    # arrange
    with device_manager_instance.monochromators[0] as monochromator:
        monochromator.home()
        while monochromator.is_busy():
            time.sleep(1)

        expected_slit_position_before = 200
        expected_slit_position_after = 300
        slit = Monochromator.Slit.A

        # act
        monochromator.set_slit_step_position(slit, expected_slit_position_before)
        while monochromator.is_busy():
            time.sleep(1)

        actual_slit_position_before = monochromator.get_slit_step_position(slit)

        monochromator.set_slit_step_position(slit, expected_slit_position_after)
        while monochromator.is_busy():
            time.sleep(1)

        actual_slit_position_after = monochromator.get_slit_step_position(slit)

        # assert
        assert actual_slit_position_before == expected_slit_position_before
        assert actual_slit_position_after == expected_slit_position_after
