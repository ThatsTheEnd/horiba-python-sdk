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
    # act
    async with device_manager_instance.monochromators[0] as monochromator:
        # assert
        assert await monochromator.is_open() is True


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_busy(device_manager_instance):
    # arrange
    async with device_manager_instance.monochromators[0] as monochromator:
        # act
        # assert
        assert await monochromator.is_busy() is False


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_config(device_manager_instance):  # noqa: ARG001
    # arrange
    async with device_manager_instance.monochromators[0] as monochromator:
        # act
        config = await monochromator.configuration()

        # assert
        assert config
        assert 'configuration' in config
        assert config['configuration'] != ''


# takes a looooot of time, which makes the websocket run into the timeout
# @pytest.mark.asyncio
# @pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
# async def test_monochromator_wavelength(device_manager_instance):
#     # arrange
#     async with device_manager_instance.monochromators[0] as monochromator:
#         # act
#         await monochromator.move_to_target_wavelength(100)
#         await asyncio.sleep(1)

#         mono_busy = False
#         while not mono_busy:
#             mono_busy = await monochromator.is_busy
#             await asyncio.sleep(0.1)

#         # assert
#         assert await monochromator.get_current_wavelength() > 0


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_calibrate_wavelength(device_manager_instance):
    # arrange
    async with device_manager_instance.monochromators[0] as monochromator:
        # act
        # TODO: How to test this properly???
        # await monochromator.calibrate_wavelength(350)

        # assert
        # assert await monochromator.get_current_wavelength() > 0
        assert await monochromator.is_busy() is False
        assert True


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
@pytest.mark.asyncio
async def test_monochromator_turret_grating_position(device_manager_instance):
    # arrange
    async with device_manager_instance.monochromators[0] as monochromator:
        # act
        # assert
        # TODO: uncomment as soon as ICL is fixed
        # await monochromator.set_turret_grating(Monochromator.Grating.FIRST)
        # assert await monochromator.get_turret_grating() == Monochromator.Grating.FIRST
        assert await monochromator.is_busy() is False


# crashes ICL, we need to know order of commands to execute before this one
# @pytest.mark.asyncio
# @pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
# async def test_monochromator_can_move_turret_grating_position(device_manager_instance):
#    # arrange
#    async with device_manager_instance.monochromators[0] as monochromator:
#        # act
#        await monochromator.set_turret_grating_position(50)
#        await asyncio.sleep(1)
#        mono_busy = False
#        while not mono_busy:
#            mono_busy = await monochromator.is_busy
#            await asyncio.sleep(0.1)

#        # assert
#        assert await monochromator.turret_grating_position >= 0


# Filter wheel not available on our mono
# @pytest.mark.asyncio
# @pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
# async def test_monochromator_filter_wheel(device_manager_instance):  # noqa: ARG001
#     # arrange
#     async with device_manager_instance.monochromators[0] as monochromator:
#         # act
#         # assert
#         assert await monochromator.get_filter_wheel_position() == Monochromator.FilterWheelPosition.RED


# Filter wheel not available on our mono
# @pytest.mark.asyncio
# @pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
# async def test_monochromator_change_filter_wheel_position(device_manager_instance):  # noqa: ARG001
#     # arrange
#     async with device_manager_instance.monochromators[0] as monochromator:
#         # act
#         await monochromator.set_filter_wheel_position(Monochromator.FilterWheelPosition.RED)
#         # assert
#         assert await monochromator.get_filter_wheel_position() == Monochromator.FilterWheelPosition.RED


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_shutter_position(device_manager_instance):
    # arrange
    async with device_manager_instance.monochromators[0] as monochromator:
        # act
        # TODO: uncomment as soon as ICL is fixed
        shutter_status = await monochromator.get_shutter_position()
        # assert
        assert (
            shutter_status == Monochromator.ShutterPosition.OPENED
            or shutter_status == Monochromator.ShutterPosition.CLOSED
        )


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_mirror_position(device_manager_instance):
    # arrange
    async with device_manager_instance.monochromators[0] as monochromator:
        # act
        # TODO: uncomment as soon as all the possible values are known
        # mirror_position: int = await monochromator.get_mirror_position(Monochromator.Mirror.FIRST)

        # assert
        # assert mirror_position == Monochromator.MirrorPosition.A
        assert await monochromator.is_busy() is False


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_change_mirror_position(device_manager_instance):
    # arrange
    async with device_manager_instance.monochromators[0] as monochromator:
        # act
        # TODO: uncomment as soon as ICL is fixed
        # await monochromator.set_mirror_position(Monochromator.Mirror.FIRST, Monochromator.MirrorPosition.A)
        # assert
        # assert await monochromator.get_mirror_position(Monochromator.Mirror.FIRST) == Monochromator.MirrorPosition.A
        assert await monochromator.is_busy() is False


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_get_slit_position(device_manager_instance):  # noqa: ARG001
    # arrange
    async with device_manager_instance.monochromators[0] as monochromator:
        # act
        # assert
        assert await monochromator.get_slit_position_in_mm(Monochromator.Slit.A) >= 0


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_set_slit_position(device_manager_instance):  # noqa: ARG001
    # arrange
    async with device_manager_instance.monochromators[0] as monochromator:
        # act
        # TODO: uncomment as soon as ICL is fixed
        # await monochromator.set_slit_position(Monochromator.Slit.A, 0.0)
        # assert
        assert await monochromator.get_slit_position_in_mm(Monochromator.Slit.A) == 0


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_get_slit_step_position(device_manager_instance):  # noqa: ARG001
    # arrange
    async with device_manager_instance.monochromators[0] as monochromator:
        # act
        # assert
        assert await monochromator.get_slit_step_position(Monochromator.Slit.A) == Monochromator.SlitStepPosition.A


@pytest.mark.asyncio
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_monochromator_set_slit_step_position(device_manager_instance):  # noqa: ARG001
    # arrange
    async with device_manager_instance.monochromators[0] as monochromator:
        # act
        # TODO: uncomment as soon as ICL is fixed
        # await monochromator.set_slit_step_position(Monochromator.Slit.A, Monochromator.SlitStepPosition.A)
        # assert
        assert await monochromator.get_slit_step_position(Monochromator.Slit.A) == Monochromator.SlitStepPosition.A
