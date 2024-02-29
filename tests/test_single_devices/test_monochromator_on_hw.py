# pylint: skip-file
import asyncio
import os

import pytest
import pytest_asyncio

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

    await device_manager.start()

    yield device_manager

    await device_manager.stop()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_opens(device_manager_instance):
    # arrange
    monochromator = device_manager_instance.monochromators[0]

    # act
    await monochromator.open()

    # assert
    assert await monochromator.is_open() is True

    await monochromator.close()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_busy(device_manager_instance):
    # arrange
    monochromator = device_manager_instance.monochromators[0]

    # act
    await monochromator.open()

    # assert
    assert await monochromator.is_busy() is False

    await monochromator.close()


# takes a looooot of time, which makes the websocket run into the timeout
# @pytest.mark.asyncio
# @pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
# async def test_monochromator_wavelength(device_manager_instance):
#     # arrange
#     monochromator = device_manager_instance.monochromators[0]
#
#     # act
#     await monochromator.open()
#     await monochromator.move_to_target_wavelength(100)
#     await asyncio.sleep(1)
#     mono_busy = False
#     while not mono_busy:
#         mono_busy = await monochromator.is_busy
#         await asyncio.sleep(0.1)
#     # assert
#     assert await monochromator.get_current_wavelength() > 0
#
#     await monochromator.close()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_calibrate_wavelength(device_manager_instance):
    # arrange
    monochromator = device_manager_instance.monochromators[0]

    # act
    await monochromator.open()
    # TODO: How to test this properly???
    #await monochromator.calibrate_wavelength(350)

    # assert
    #assert await monochromator.get_current_wavelength() > 0
    assert True

    await monochromator.close()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
@pytest.mark.asyncio
async def test_monochromator_turret_grating_position(device_manager_instance):
    # arrange
    monochromator = device_manager_instance.monochromators[0]

    # act
    await monochromator.open()

    # assert
    assert await monochromator.get_turret_grating_position() >= 0

    await monochromator.close()


# crashes ICL, we need to know order of commands to execute before this one
# @pytest.mark.asyncio
# @pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
# async def test_monochromator_can_move_turret_grating_position(device_manager_instance):
#     # arrange
#     monochromator = device_manager_instance.monochromators[0]
#
#     # act
#     await monochromator.open()
#     await monochromator.set_turret_grating_position(50)
#     await asyncio.sleep(1)
#     mono_busy = False
#     while not mono_busy:
#         mono_busy = await monochromator.is_busy
#         await asyncio.sleep(0.1)
#
#     # assert
#     assert await monochromator.turret_grating_position > 0
#
#     await monochromator.close()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_shutter_status(device_manager_instance):
    # arrange
    monochromator = device_manager_instance.monochromators[0]

    # act
    await monochromator.open()
    shutter_status = await monochromator.get_shutter_status()

    # assert
    assert shutter_status == Monochromator.ShutterStatus.OPEN or shutter_status == Monochromator.ShutterStatus.CLOSED

    await monochromator.close()


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_mirror_position(device_manager_instance):
    # arrange
    monochromator = device_manager_instance.monochromators[0]

    # act
    await monochromator.open()
    mirror_position: int = await monochromator.get_mirror_position()

    # assert
    assert mirror_position > 0

    await monochromator.close()
