# pylint: skip-file
# Important note: the FakeDeviceManager will return the contents of the
# horiba_sdk/devices/fake_responses/monochromator.json
import threading

import pytest
from numericalunits import nm

from horiba_sdk.devices import FakeDeviceManager
from horiba_sdk.devices.single_devices import Monochromator

fake_icl_host: str = 'localhost'
fake_icl_port: int = 8766
fake_icl_uri: str = 'ws://' + fake_icl_host + ':' + str(fake_icl_port)


@pytest.fixture(scope='module')
def fake_device_manager():
    fake_device_manager = FakeDeviceManager(fake_icl_host, fake_icl_port)
    return fake_device_manager


@pytest.fixture(scope='module')
def _run_fake_icl_server(fake_device_manager):
    thread = threading.Thread(target=fake_device_manager.start_icl)
    thread.start()
    yield
    fake_device_manager.loop.call_soon_threadsafe(fake_device_manager.server.cancel)
    thread.join()


@pytest.mark.asyncio
async def test_monochromator_opens(fake_device_manager, _run_fake_icl_server):
    # arrange
    monochromator = Monochromator(fake_device_manager)

    # act
    await monochromator.open(1)

    # assert
    assert await monochromator.is_open is True

    await monochromator.close()


@pytest.mark.asyncio
async def test_monochromator_busy(fake_device_manager, _run_fake_icl_server):
    # arrange
    monochromator = Monochromator(fake_device_manager)

    # act
    await monochromator.open(1)

    # assert
    assert await monochromator.is_busy is True

    await monochromator.close()


@pytest.mark.asyncio
async def test_monochromator_wavelength(fake_device_manager, _run_fake_icl_server):
    # arrange
    monochromator = Monochromator(fake_device_manager)

    # act
    await monochromator.open(1)

    # assert
    assert await monochromator.wavelength > 0

    await monochromator.close()


@pytest.mark.asyncio
async def test_monochromator_can_move_to_wavelength(fake_device_manager, _run_fake_icl_server):
    # arrange
    monochromator = Monochromator(fake_device_manager)

    # act
    await monochromator.open(1)
    await monochromator.move_to_wavelength(350 * nm)

    # assert
    assert await monochromator.wavelength > 0

    await monochromator.close()


@pytest.mark.asyncio
async def test_monochromator_turret_grating_position(fake_device_manager, _run_fake_icl_server):
    # arrange
    monochromator = Monochromator(fake_device_manager)

    # act
    await monochromator.open(1)

    # assert
    assert await monochromator.turret_grating_position > 0

    await monochromator.close()


@pytest.mark.asyncio
async def test_monochromator_can_move_turret_grating_position(fake_device_manager, _run_fake_icl_server):
    # arrange
    monochromator = Monochromator(fake_device_manager)

    # act
    await monochromator.open(1)
    await monochromator.move_turret_to_grating(50)

    # assert
    assert await monochromator.turret_grating_position > 0

    await monochromator.close()
