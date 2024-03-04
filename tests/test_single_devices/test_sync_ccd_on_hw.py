# pylint: skip-file

import os

import pytest

from horiba_sdk import ureg
from horiba_sdk.sync.devices import DeviceManager


@pytest.fixture(scope='module')
def device_manager_instance():
    device_manager = DeviceManager(start_icl=True)

    device_manager.start()

    yield device_manager

    device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_ccd_opens(device_manager_instance):  # noqa: ARG001
    # arrange
    # act
    with device_manager_instance.charge_coupled_devices[0] as ccd:
        # assert
        assert ccd.is_open() is True


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_ccd_temperature(device_manager_instance):  # noqa: ARG001
    # arrange
    # act
    with device_manager_instance.charge_coupled_devices[0] as ccd:
        # assert
        temperature = ccd.get_temperature()
        zero = ureg.Quantity(0, ureg.degC)
        assert temperature != zero


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_ccd_resolution(device_manager_instance):  # noqa: ARG001
    # arrange
    # act
    with device_manager_instance.charge_coupled_devices[0] as ccd:
        # assert
        resolution = ccd.get_chip_size()
        assert resolution.width > 0 and resolution.height > 0


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_ccd_speed(device_manager_instance):  # noqa: ARG001
    # arrange
    # act
    with device_manager_instance.charge_coupled_devices[0] as ccd:
        # assert
        speed = ccd.get_speed()
        zero = ureg.Quantity(0, ureg.kHz)
        assert speed != zero
