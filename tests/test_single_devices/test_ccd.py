# pylint: skip-file
# Important note: the FakeDeviceManager will return the contents of the
# horiba_sdk/devices/fake_responses/ccd.json
import threading

import pytest

from horiba_sdk import ureg
from horiba_sdk.devices import FakeDeviceManager
from horiba_sdk.devices.single_devices import ChargeCoupledDevice

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
async def test_ccd_opens(fake_device_manager, _run_fake_icl_server):
    # arrange
    # act
    async with ChargeCoupledDevice(fake_device_manager) as ccd:
        # assert
        await ccd.open(1, enable_binary_messages=True)
        assert await ccd.is_open() is True


@pytest.mark.asyncio
async def test_ccd_temperature(fake_device_manager, _run_fake_icl_server):
    # arrange
    # act
    async with ChargeCoupledDevice(fake_device_manager) as ccd:
        await ccd.open(1, enable_binary_messages=True)
        # assert
        temperature = await ccd.get_temperature()
        zero = ureg.Quantity(0, ureg.degC)
        assert temperature != zero


@pytest.mark.asyncio
async def test_ccd_resolution(fake_device_manager, _run_fake_icl_server):
    # arrange
    # act
    async with ChargeCoupledDevice(fake_device_manager) as ccd:
        await ccd.open(1, enable_binary_messages=True)
        # assert
        resolution = await ccd.get_chip_size()
        assert resolution.width > 0 and resolution.height > 0


@pytest.mark.asyncio
async def test_ccd_speed(fake_device_manager, _run_fake_icl_server):
    # arrange
    # act
    async with ChargeCoupledDevice(fake_device_manager) as ccd:
        await ccd.open(1, enable_binary_messages=True)
        # assert
        speed = await ccd.get_speed()
        zero = ureg.Quantity(0, ureg.kHz)
        assert speed != zero
