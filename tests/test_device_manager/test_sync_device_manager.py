# pylint: skip-file

import os

import psutil
import pytest

from horiba_sdk.communication import Command
from horiba_sdk.sync.devices import DeviceManager


def is_icl_running() -> bool:
    return any(process.info['name'] == 'icl.exe' for process in psutil.process_iter(['pid', 'name']))


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_device_manager_start_icl(event_loop):  # noqa: ARG001
    device_manager = DeviceManager(start_icl=True)
    device_manager.start()
    assert is_icl_running(), 'ICL software is not running on the system'
    device_manager.stop()
    assert not is_icl_running(), 'ICL software is still running on the system'


def test_device_manager_with_fake_icl_exe(fake_sync_icl_exe, fake_icl_host_fixture, fake_icl_port_fixture):  # noqa: ARG001
    device_manager = DeviceManager(
        start_icl=False, websocket_ip=fake_icl_host_fixture, websocket_port=fake_icl_port_fixture
    )
    device_manager.start()
    communicator = device_manager.communicator

    info_response = communicator.request_with_response(Command('icl_info', {}))

    assert 'nodeVersion' in info_response.results
    assert communicator.opened()
    assert len(device_manager.charge_coupled_devices) == 1  # defined in horiba_sdk/devices/fake_responses/ccd.json
    assert len(device_manager.monochromators) == 1  # defined in horiba_sdk/devices/fake_responses/monochromator.json

    device_manager.stop()
    assert not communicator.opened()
