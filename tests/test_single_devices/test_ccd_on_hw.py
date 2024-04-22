import asyncio
import os
import random

import pytest
from loguru import logger

from horiba_sdk.core.gain import Gain
from horiba_sdk.core.speed import Speed
from horiba_sdk.devices.device_manager import DeviceManager
from horiba_sdk.devices.single_devices.ccd import ChargeCoupledDevice


# Tell pytest to run this test only if called from the scope of this module. If any other pytest scope calls this test,
# ignore it
@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_functionality(event_loop):  # noqa: ARG001
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            # act
            chip_size = await ccd.get_chip_size()
            assert chip_size.width > 0 and chip_size.height > 0

            new_exposure_time = random.randint(1000, 5000)
            await ccd.set_exposure_time(new_exposure_time)
            assert await ccd.get_exposure_time() == new_exposure_time

            temperature = await ccd.get_temperature()
            assert temperature < 0

            _ignored_speed = await ccd.get_speed()

            await ccd.set_acquisition_format(1, ChargeCoupledDevice.AcquisitionFormat.IMAGE)
            await ccd.set_region_of_interest()

            if await ccd.get_acquisition_ready():
                await ccd.set_acquisition_start(open_shutter=True)
                await asyncio.sleep(1)  # Wait a short period for the acquisition to start

                acquisition_busy = True
                while acquisition_busy:
                    acquisition_busy = await ccd.get_acquisition_busy()
                    await asyncio.sleep(0.3)
                    logger.info('Acquisition busy')

                acquisition_data_size = await ccd.get_acquisition_data_size()
                acquisition_data = await ccd.get_acquisition_data()

                assert acquisition_data_size > 0
                assert acquisition_data['acquisition'][0]['xOrigin'] == 0
                assert acquisition_data['acquisition'][0]['yOrigin'] == 0
    finally:
        await device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_speed(event_loop):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            # act
            await ccd.set_speed(Speed.SyncerityOE._45_KHZ)
            speed_before = await ccd.get_speed(Speed.SyncerityOE)

            await ccd.set_speed(Speed.SyncerityOE._1_MHZ)
            speed_after = await ccd.get_speed(Speed.SyncerityOE)

            # assert
            assert speed_before == Speed.SyncerityOE._45_KHZ
            assert speed_before != Speed.SynapsePlus._50_KHZ_HS
            assert speed_after == Speed.SyncerityOE._1_MHZ
            assert speed_after != Speed.SynapsePlus._50_KHZ_HS
    finally:
        await device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_gain(event_loop):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            # act
            await ccd.set_gain(Gain.SyncerityOE.HIGH_SENSITIVITY)
            gain_before = await ccd.get_gain(Gain.SyncerityOE)

            await ccd.set_gain(Gain.SyncerityOE.HIGH_LIGHT)
            gain_after = await ccd.get_gain(Gain.SyncerityOE)

            # assert
            assert gain_before == Gain.SyncerityOE.HIGH_SENSITIVITY
            assert gain_after == Gain.SyncerityOE.HIGH_LIGHT
            assert gain_before != Gain.SynapsePlus.ULTIMATE_SENSITIVITY
            assert gain_after != Gain.SynapsePlus.ULTIMATE_SENSITIVITY
    finally:
        await device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_resolution(event_loop):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            # act
            resolution = await ccd.get_chip_size()
            config = await ccd.get_configuration()

            # assert
            assert resolution.width == config['ChipWidth']
            assert resolution.height == config['ChipHeight']
    finally:
        await device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_temperature(event_loop):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            # act
            temperature = await ccd.get_chip_temperature()

            # assert
            assert temperature < 0
    finally:
        await device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_fit_parameters(event_loop):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            expected_fit_params_before = [1, 0, 0, 0, 0]
            expected_fit_params_after = [0, 0, 1, 0, 0]

            # act
            await ccd.set_fit_parameters(expected_fit_params_before)
            actual_fit_params_before = await ccd.get_fit_parameters()

            await ccd.set_fit_parameters(expected_fit_params_after)
            actual_fit_params_after = await ccd.get_fit_parameters()

            # assert
            assert actual_fit_params_before == expected_fit_params_before
            assert actual_fit_params_after == expected_fit_params_after
    finally:
        await device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_timer_resolution(event_loop):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            expected_timer_resolution_before = ChargeCoupledDevice.TimerResolution._1_MICROSECONDS
            expected_timer_resolution_after = ChargeCoupledDevice.TimerResolution._1000_MICROSECONDS

            # act
            await ccd.set_timer_resolution(ChargeCoupledDevice.TimerResolution._1_MICROSECONDS)
            actual_timer_resolution_before = await ccd.get_timer_resolution()

            await ccd.set_timer_resolution(ChargeCoupledDevice.TimerResolution._1000_MICROSECONDS)
            actual_timer_resolution_after = await ccd.get_timer_resolution()

            # assert
            assert actual_timer_resolution_before == expected_timer_resolution_before
            assert actual_timer_resolution_after == expected_timer_resolution_after
    finally:
        await device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_exposure_time(event_loop):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            await ccd.set_timer_resolution(ChargeCoupledDevice.TimerResolution._1000_MICROSECONDS)
            expected_exposure_time_before = 100
            expected_exposure_time_after = 110

            # act
            await ccd.set_exposure_time(expected_exposure_time_before)
            actual_exposure_time_before = await ccd.get_exposure_time()

            await ccd.set_exposure_time(expected_exposure_time_after)
            actual_exposure_time_after = await ccd.get_exposure_time()

            # assert
            assert actual_exposure_time_before == expected_exposure_time_before
            assert actual_exposure_time_after == expected_exposure_time_after
    finally:
        await device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_roi(event_loop):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            await ccd.set_exposure_time(100)
            await ccd.set_acquisition_format(1, ChargeCoupledDevice.AcquisitionFormat.IMAGE)
            # act
            await ccd.set_region_of_interest(0, 0, 0, 1000, 200, 1, 200)
            if await ccd.get_acquisition_ready():
                await ccd.set_acquisition_start(open_shutter=True)
                await asyncio.sleep(1)  # Wait a short period for the acquisition to start

                acquisition_busy = True
                while acquisition_busy:
                    acquisition_busy = await ccd.get_acquisition_busy()
                    await asyncio.sleep(0.3)
                    logger.info('Acquisition busy')

                acquisition_data_size = await ccd.get_acquisition_data_size()
                acquisition_data = await ccd.get_acquisition_data()

                assert acquisition_data_size == 1000
                assert acquisition_data['acquisition'][0]['xOrigin'] == 0
                assert acquisition_data['acquisition'][0]['yOrigin'] == 0
                assert acquisition_data['acquisition'][0]['xSize'] == 1000
                assert acquisition_data['acquisition'][0]['ySize'] == 200
                assert acquisition_data['acquisition'][0]['xBinning'] == 1
                assert acquisition_data['acquisition'][0]['yBinning'] == 200

    finally:
        await device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_x_axis_conversion_type(event_loop):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            expected_x_axis_conversion_type_before = ChargeCoupledDevice.XAxisConversionType.NONE
            expected_x_axis_conversion_type_after = ChargeCoupledDevice.XAxisConversionType.FROM_CCD_FIRMWARE

            # act
            await ccd.set_x_axis_conversion_type(expected_x_axis_conversion_type_before)
            actual_x_axis_conversion_type_before = await ccd.get_x_axis_conversion_type()

            await ccd.set_x_axis_conversion_type(expected_x_axis_conversion_type_after)
            actual_x_axis_conversion_type_after = await ccd.get_x_axis_conversion_type()

            assert actual_x_axis_conversion_type_before == expected_x_axis_conversion_type_before
            assert actual_x_axis_conversion_type_after == expected_x_axis_conversion_type_after
    finally:
        await device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_acquisition_count(event_loop):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            expected_acquisition_count_before = 1
            expected_acquisition_count_after = 2

            # act
            ccd.set_acquisition_count(expected_acquisition_count_before)
            actual_acquisition_count_before = await ccd.get_acquisition_count()

            ccd.set_acquisition_count(expected_acquisition_count_after)
            actual_acquisition_count_after = await ccd.get_acquisition_count()

            assert actual_acquisition_count_before == expected_acquisition_count_before
            assert actual_acquisition_count_after == expected_acquisition_count_after
    finally:
        await device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_clean_count(event_loop):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            expected_clean_count_before = 1
            expected_clean_count_after = 2

            # act
            ccd.set_clean_count(expected_clean_count_before)
            actual_clean_count_before = await ccd.get_clean_count()

            ccd.set_clean_count(expected_clean_count_after)
            actual_clean_count_after = await ccd.get_clean_count()

            assert actual_clean_count_before == expected_clean_count_before
            assert actual_clean_count_after == expected_clean_count_after
    finally:
        await device_manager.stop()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
async def test_ccd_trigger_in(event_loop):  # noqa: ARG001
    # arrange
    device_manager = DeviceManager()
    try:
        await device_manager.start()

        async with device_manager.charge_coupled_devices[0] as ccd:
            expected_trigger_input_before = (False, -1, -1, -1)
            (
                expected_enabled_before,
                expected_address_before,
                expected_event_before,
                expected_signal_type_before,
            ) = expected_trigger_input_before

            expected_trigger_input_after = (True, 0, 0, 0)
            (
                expected_enabled_after,
                expected_address_after,
                expected_event_after,
                expected_signal_type_after,
            ) = expected_trigger_input_after

            # act
            await ccd.set_trigger_input(
                expected_enabled_before, expected_address_before, expected_event_before, expected_signal_type_before
            )
            actual_trigger_input_before = await ccd.get_trigger_input()

            await ccd.set_trigger_input(
                expected_enabled_after, expected_address_after, expected_event_after, expected_signal_type_after
            )
            actual_trigger_input_after = await ccd.get_trigger_input()

            assert actual_trigger_input_before == expected_trigger_input_before
            assert actual_trigger_input_after == expected_trigger_input_after

    finally:
        await device_manager.stop()
