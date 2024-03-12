# pylint: skip-file
# Important note: the fake_icl_exe will return the contents of the
# horiba_sdk/devices/fake_responses/monochromator.json
# Look at /test/conftest.py for the definition of fake_icl_exe


from horiba_sdk.devices.monochromator_discovery import MonochromatorsDiscovery
from horiba_sdk.icl_error import FakeErrorDB


async def test_mono_discovery_executes(fake_icl_exe, fake_device_manager):  # noqa: ARG001
    # arrange
    fake_error_db = FakeErrorDB()
    mono_discovery = MonochromatorsDiscovery(fake_device_manager.communicator, fake_error_db)

    # act
    await mono_discovery.execute()

    # assert
    assert len(mono_discovery.monochromators()) != 0
