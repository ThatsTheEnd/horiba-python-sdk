# pylint: skip-file

import os

import psutil
import pytest

from horiba_sdk.devices import DeviceManager


# This fixture ensures DeviceManager is clean for each test
@pytest.fixture(autouse=True)
def clean_singleton():
    DeviceManager.clear_instances()


def is_icl_running() -> bool:
    return any(process.info['name'] == 'icl.exe' for process in psutil.process_iter(['pid', 'name']))


def test_singleton_device_manager():
    device_manager_1 = DeviceManager(start_icl=False)
    device_manager_2 = DeviceManager(start_icl=False)
    assert device_manager_1 is device_manager_2


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_device_manager_start_icl():
    device_manager = DeviceManager(start_icl=True)
    assert is_icl_running(), 'ICL software is not running on the system'
    device_manager.stop_icl()
