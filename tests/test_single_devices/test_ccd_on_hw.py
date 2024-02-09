# pylint: skip-file
import os

import pytest

from horiba_sdk import ureg
from horiba_sdk.devices import DeviceManager
from horiba_sdk.devices.single_devices import ChargeCoupledDevice


@pytest.fixture(scope='module')
def device_manager():
    device_manager = DeviceManager(start_icl=True)
    return device_manager


@pytest.fixture(scope='module')
def _startup_and_teardown(device_manager):
    # startup before all tests
    yield
    # teardown after all tests
    device_manager.stop_icl()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_opens(device_manager):
    # arrange
    # act
    async with ChargeCoupledDevice(device_manager) as ccd:
        # assert
        await ccd.open(0, enable_binary_messages=True)
        assert await ccd.is_open() is True


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_temperature(device_manager, _startup_and_teardown):
    # arrange
    # act
    async with ChargeCoupledDevice(device_manager) as ccd:
        await ccd.open(0, enable_binary_messages=True)
        # assert
        temperature = await ccd.get_temperature()
        zero = ureg.Quantity(0, ureg.degC)
        assert temperature != zero


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_resolution(device_manager, _startup_and_teardown):
    # arrange
    # act
    async with ChargeCoupledDevice(device_manager) as ccd:
        await ccd.open(0, enable_binary_messages=True)
        # assert
        resolution = await ccd.get_chip_size()
        assert resolution.width > 0 and resolution.height > 0


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_speed(device_manager, _startup_and_teardown):
    # arrange
    # act
    async with ChargeCoupledDevice(device_manager) as ccd:
        await ccd.open(0, enable_binary_messages=True)
        # assert
        speed = await ccd.get_speed()
        zero = ureg.Quantity(0, ureg.kHz)
        assert speed != zero
