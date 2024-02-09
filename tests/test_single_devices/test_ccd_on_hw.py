# pylint: skip-file
import asyncio
import os

import pytest
import pytest_asyncio

from horiba_sdk import ureg
from horiba_sdk.devices import DeviceManager
from horiba_sdk.devices.single_devices import ChargeCoupledDevice


@pytest.fixture(scope='session')
def event_loop(_request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='module')
async def device_manager_instance():
    device_manager = DeviceManager(start_icl=True)

    await device_manager.communicator.open()
    await device_manager.discover_devices()

    yield device_manager

    await device_manager.stop_icl()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_opens(device_manager_instance):
    # arrange
    # act
    async with ChargeCoupledDevice(device_manager_instance) as ccd:
        # assert
        await ccd.open(0, enable_binary_messages=True)
        assert await ccd.is_open() is True


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_temperature(device_manager_instance):
    # arrange
    # act
    async with ChargeCoupledDevice(device_manager_instance) as ccd:
        await ccd.open(0, enable_binary_messages=True)
        # assert
        temperature = await ccd.get_temperature()
        zero = ureg.Quantity(0, ureg.degC)
        assert temperature != zero


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_resolution(device_manager_instance):
    # arrange
    # act
    async with ChargeCoupledDevice(device_manager_instance) as ccd:
        await ccd.open(0, enable_binary_messages=True)
        # assert
        resolution = await ccd.get_chip_size()
        assert resolution.width > 0 and resolution.height > 0


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_speed(device_manager_instance):
    # arrange
    # act
    async with ChargeCoupledDevice(device_manager_instance) as ccd:
        await ccd.open(0, enable_binary_messages=True)
        # assert
        speed = await ccd.get_speed()
        zero = ureg.Quantity(0, ureg.kHz)
        assert speed != zero
