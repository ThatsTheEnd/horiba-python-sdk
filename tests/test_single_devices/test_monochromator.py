# pylint: skip-file
# Important note: the FakeDeviceManager will return the contents of the
# horiba_sdk/devices/fake_responses/monochromator.json
import pytest
from numericalunits import nm


@pytest.mark.asyncio
async def test_monochromator_opens(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    monochromator = fake_device_manager.monochromators[0]

    # act
    await monochromator.open()

    # assert
    assert await monochromator.is_open() is True

    await monochromator.close()


@pytest.mark.asyncio
async def test_monochromator_busy(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    monochromator = fake_device_manager.monochromators[0]

    # act
    await monochromator.open()

    # assert
    assert await monochromator.is_busy is True

    await monochromator.close()


@pytest.mark.asyncio
async def test_monochromator_wavelength(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    monochromator = fake_device_manager.monochromators[0]

    # act
    await monochromator.open()

    # assert
    assert await monochromator.wavelength > 0

    await monochromator.close()


@pytest.mark.asyncio
async def test_monochromator_can_move_to_wavelength(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    monochromator = fake_device_manager.monochromators[0]

    # act
    await monochromator.open()
    await monochromator.move_to_wavelength(350 * nm)

    # assert
    assert await monochromator.wavelength > 0

    await monochromator.close()


@pytest.mark.asyncio
async def test_monochromator_turret_grating_position(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    monochromator = fake_device_manager.monochromators[0]

    # act
    await monochromator.open()

    # assert
    assert await monochromator.turret_grating_position > 0

    await monochromator.close()


@pytest.mark.asyncio
async def test_monochromator_can_move_turret_grating_position(fake_device_manager, fake_icl_exe):  # noqa: ARG001
    # arrange
    monochromator = fake_device_manager.monochromators[0]

    # act
    await monochromator.open()
    await monochromator.move_turret_to_grating(50)

    # assert
    assert await monochromator.turret_grating_position > 0

    await monochromator.close()
