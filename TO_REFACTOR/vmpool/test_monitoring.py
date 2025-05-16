import pytest
from time            import sleep
from typing          import List
from api             import One
from utils           import get_unic_name
from one_cli.vm      import VirtualMachine
from one_cli.image   import Image, create_image
from config          import ADMIN_NAME, VmStates


VM_MONITOR_INTERVAL = 30 # Param MONITOR_VM in /etc/one/monitord.conf



@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def image(one: One):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = one.image.allocate(template, 1)
    while one.image.info(image_id).STATE != 1: sleep(0.5)
    yield Image(image_id)
    while one.image.info(image_id).STATE != 1: sleep(0.5)
    one.image.delete(image_id)




@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def vms_with_disk(one: One, image: Image):
    vms_list = []

    for _ in range(5):
        vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=0.1\nMEMORY=1\nDISK=[IMAGE_ID={image._id}]")
        vms_list.append(VirtualMachine(vm_id))
        while one.vm.info(vm_id).STATE != VmStates.POWEROFF: sleep(0.5)

    yield vms_list

    for vm in vms_list:
        one.vm.action("terminate-hard", vm._id)
        while one.vm.info(vm._id).STATE != VmStates.DONE: sleep(0.5)





# =================================================================================================
# TESTS
# =================================================================================================

@pytest.mark.parametrize("filtration", [-4, -3, -2, -1, 0, 1, 9999])
@pytest.mark.parametrize("last_secs", [-1, 0, 9999])
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_monitoring_filters(one: One, filtration: int, last_secs: int):
    one.vmpool.monitoring(filtration, last_secs)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_monitoring_changes(one: One, vms_with_disk: List[VirtualMachine]):
    records_before = one.vmpool.monitoring(last_seconds=-1).MONITORING
    sleep(VM_MONITOR_INTERVAL * 2.5)
    records_after  = one.vmpool.monitoring(last_seconds=-1).MONITORING
    assert len(records_before) < len(records_after)
    