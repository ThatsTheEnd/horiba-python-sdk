# pylint: skip-file
import asyncio
import threading

import pytest

from horiba_sdk.devices import FakeDeviceManager
from horiba_sdk.devices.fake_icl_server import FakeICLServer
from horiba_sdk.sync.devices import FakeDeviceManager as FakeSyncDeviceManager
from horiba_sdk.sync.devices.fake_icl_server import FakeICLServer as FakeSyncICLServer

fake_icl_host: str = 'localhost'
fake_icl_port: int = 8766
fake_icl_uri: str = 'ws://' + fake_icl_host + ':' + str(fake_icl_port)


@pytest.fixture(scope='module')
def fake_icl_host_fixture():
    return fake_icl_host


@pytest.fixture(scope='module')
def fake_icl_port_fixture():
    return fake_icl_port


@pytest.fixture(scope='module')
def fake_icl_uri_fixture():
    return fake_icl_uri


@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='module')
async def fake_icl_exe(event_loop):  # noqa: ARG001
    server = FakeICLServer(fake_icl_host=fake_icl_host, fake_icl_port=fake_icl_port)
    await server.start()

    yield server

    await server.stop()


@pytest.fixture(scope='module')
async def fake_device_manager(event_loop):  # noqa: ARG001
    fake_device_manager = FakeDeviceManager(host=fake_icl_host, port=fake_icl_port)

    yield fake_device_manager


@pytest.fixture(scope='module')
def fake_sync_icl_exe():  # noqa: ARG001
    sync_server = FakeSyncICLServer(fake_icl_host=fake_icl_host, fake_icl_port=fake_icl_port)
    thread = threading.Thread(target=sync_server.start)
    thread.start()

    yield thread

    sync_server.stop()
    thread.join()


@pytest.fixture(scope='module')
def fake_sync_device_manager():  # noqa: ARG001
    fake_device_manager = FakeSyncDeviceManager(host=fake_icl_host, port=fake_icl_port)
    fake_device_manager.start()

    yield fake_device_manager
    fake_device_manager.stop()
