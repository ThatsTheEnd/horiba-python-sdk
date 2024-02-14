# pylint: skip-file
import asyncio
import os

import pytest
import pytest_asyncio

from horiba_sdk import ureg
from horiba_sdk.devices import DeviceManager
from horiba_sdk.devices.single_devices import ChargeCoupledDevice


@pytest.fixture(scope='session')
def event_loop(request):  # noqa: ARG001
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
    async with device_manager_instance.charge_coupled_devices[0] as ccd:
        # assert
        assert await ccd.is_open() is True


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_temperature(device_manager_instance):
    # arrange
    # act
    async with device_manager_instance.charge_coupled_devices[0] as ccd:
        # assert
        temperature = await ccd.get_temperature()
        zero = ureg.Quantity(0, ureg.degC)
        assert temperature != zero


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_resolution(device_manager_instance):
    # arrange
    # act
    async with device_manager_instance.charge_coupled_devices[0] as ccd:
        # assert
        resolution = await ccd.get_chip_size()
        assert resolution.width > 0 and resolution.height > 0


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_speed(device_manager_instance):
    # arrange
    # act
    async with device_manager_instance.charge_coupled_devices[0] as ccd:
        # assert
        speed = await ccd.get_speed()
        zero = ureg.Quantity(0, ureg.kHz)
        assert speed != zero


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_exposure_time(device_manager_instance):
    # arrange
    # act
    async with device_manager_instance.charge_coupled_devices[0] as ccd:
        await ccd.set_exposure_time(400)
        exposure_time = await ccd.get_exposure_time()
        # assert
        assert exposure_time == 400 * ureg.milliseconds


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_x_axis_conversion_type(device_manager_instance):
    # arrange
    # act
    async with device_manager_instance.charge_coupled_devices[0] as ccd:
        await ccd.set_x_axis_conversion_type(ChargeCoupledDevice.XAxisConversionType.FROM_ICL_SETTINGS_INI)
        x_axis_conversion_type = await ccd.get_x_axis_conversion_type()
        # assert
        assert x_axis_conversion_type == ChargeCoupledDevice.XAxisConversionType.FROM_ICL_SETTINGS_INI
