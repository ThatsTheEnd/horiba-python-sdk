# pylint: skip-file
import asyncio
import os

import pytest
import pytest_asyncio
from numericalunits import nm

from horiba_sdk.devices import DeviceManager
from horiba_sdk.devices.single_devices import Monochromator


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
async def test_monochromator_opens(device_manager_instance):
    # arrange
    monochromator = Monochromator(device_manager_instance)

    # act
    await monochromator.open(0)

    # assert
    assert await monochromator.is_open is True

    await monochromator.close()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_busy(device_manager_instance):
    # arrange
    monochromator = Monochromator(device_manager_instance)

    # act
    await monochromator.open(0)

    # assert
    assert await monochromator.is_busy is True

    await monochromator.close()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_wavelength(device_manager_instance):
    # arrange
    monochromator = Monochromator(device_manager_instance)

    # act
    await monochromator.open(0)

    # assert
    assert await monochromator.wavelength > 0

    await monochromator.close()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_can_move_to_wavelength(device_manager_instance):
    # arrange
    monochromator = Monochromator(device_manager_instance)

    # act
    await monochromator.open(0)
    await monochromator.move_to_wavelength(350 * nm)

    # assert
    assert await monochromator.wavelength > 0

    await monochromator.close()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
@pytest.mark.asyncio
async def test_monochromator_turret_grating_position(device_manager_instance):
    # arrange
    monochromator = Monochromator(device_manager_instance)

    # act
    await monochromator.open(0)

    # assert
    assert await monochromator.turret_grating_position > 0

    await monochromator.close()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_can_move_turret_grating_position(device_manager_instance):
    # arrange
    monochromator = Monochromator(device_manager_instance)

    # act
    await monochromator.open(0)
    await monochromator.move_turret_to_grating(50)

    # assert
    assert await monochromator.turret_grating_position > 0

    await monochromator.close()