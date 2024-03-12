# pylint: skip-file
# Important note: the fake_icl_exe will return the contents of the
# horiba_sdk/devices/fake_responses/ccd.json
# Look at /test/conftest.py for the definition of fake_icl_exe


from horiba_sdk.devices.ccd_discovery import ChargeCoupledDevicesDiscovery
from horiba_sdk.icl_error import FakeErrorDB


async def test_ccd_discovery_executes(fake_icl_exe, fake_device_manager):  # noqa: ARG001
    # arrange
    fake_error_db = FakeErrorDB()
    ccd_discovery = ChargeCoupledDevicesDiscovery(fake_device_manager.communicator, fake_error_db)

    # act
    await ccd_discovery.execute()

    # assert
    assert len(ccd_discovery.charge_coupled_devices()) != 0
