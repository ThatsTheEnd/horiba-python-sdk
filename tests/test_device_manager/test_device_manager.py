# pylint: skip-file

import os
import platform
import subprocess
import time

import pytest

from horiba_sdk.devices import DeviceManager


# This fixture ensures DeviceManager is clean for each test
@pytest.fixture(autouse=True)
def clean_singleton():
    DeviceManager._instances = {}  # Clear the Singleton instances


def is_icl_running() -> bool:
    # This function checks if the acl.exe is running on the system
    try:
        result = subprocess.run(['tasklist'], stdout=subprocess.PIPE)
        time.sleep(0.5)
        return 'icl.exe' in result.stdout.decode()
    except Exception:
        return False


#
# def test_singleton_device_manager():
#     device_manager_1 = DeviceManager(communicator_cls=MockedTelnetCommunicator, start_acl=False)
#     device_manager_2 = DeviceManager(communicator_cls=MockedTelnetCommunicator, start_acl=False)
#     assert device_manager_1 is device_manager_2
#     device_manager_1.stop_acl()


@pytest.mark.skipif(os.environ.get('HAS_HARDWARE') != 'true', reason='Hardware tests only run locally')
def test_device_manager_start_acl():
    device_manager = DeviceManager(start_acl=True) if platform.system() == 'Windows' else DeviceManager(start_acl=False)
    assert is_icl_running(), 'ACL software is not running on the system'

    print(device_manager)
    # assert not is_acl_running(), "Failed to close ACL software"  # This only disconnects from the ACL, not stops it
