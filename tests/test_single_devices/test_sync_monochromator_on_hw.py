# pylint: skip-file

import os

import pytest

from horiba_sdk.sync.devices import DeviceManager


@pytest.fixture(scope='module')
def device_manager_instance():
    device_manager = DeviceManager(start_icl=True)

    device_manager.start()

    yield device_manager

    device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_opens(device_manager_instance):  # noqa: ARG001
    # arrange
    # act
    with device_manager_instance.monochromators[0] as monochromator:
        # assert
        assert monochromator.is_open() is True


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_busy(device_manager_instance):  # noqa: ARG001
    # arrange
    # act
    with device_manager_instance.monochromators[0] as monochromator:
        # assert
        assert monochromator.is_busy is False


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_wavelength(device_manager_instance):  # noqa: ARG001
    # arrange
    # act
    with device_manager_instance.monochromators[0] as monochromator:
        # assert
        monochromator.move_to_wavelength(0.0)
        assert abs(monochromator.wavelength - 0.0) < 1e-2


# TODO: Test is commented out until more is known about moving to the desired wavelength and max time it can take
# def test_monochromator_can_move_to_wavelength(fake_sync_icl_exe, fake_sync_device_manager):  # noqa: ARG001
#     # arrange
#     # act
#     with device_manager_instance.monochromators[0] as monochromator:
#         monochromator.move_to_wavelength(350 * nm)
#         time.sleep(15)
#         # assert
#         assert monochromator.wavelength > 0


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_turret_grating_position(device_manager_instance):  # noqa: ARG001
    # arrange
    # act
    with device_manager_instance.monochromators[0] as monochromator:
        # assert
        assert monochromator.turret_grating_position >= 0.0


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_monochromator_can_move_turret_grating_position(device_manager_instance):  # noqa: ARG001
    # arrange
    # act
    with device_manager_instance.monochromators[0] as monochromator:
        monochromator.move_turret_to_grating(5)
        # assert
        assert monochromator.turret_grating_position >= 0.0
