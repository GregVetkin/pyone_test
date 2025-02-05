import pytest
from time            import sleep
from typing          import List
from api             import One
from utils           import get_unic_name
from one_cli.vm      import VirtualMachine
from config          import ADMIN_NAME




@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def vms(one: One):
    vms_list = []

    for _ in range(5):
        vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=0.1\nMEMORY=1\n")
        vms_list.append(VirtualMachine(vm_id))

    yield vms_list

    for vm in vms_list:
        one.vm.action("terminate-hard", vm._id)





# =================================================================================================
# TESTS
# =================================================================================================

@pytest.mark.parametrize("filtration", [-4, -3, -2, -1, 0, 1, 9999])
@pytest.mark.parametrize("last_secs", [-1, 0, 9999])
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_monitoring(one: One, filtration: int, last_secs: int):
    one.vmpool.monitoring(filtration, last_secs)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_monitoring_changes(one: One, vms: List[VirtualMachine]):
    lines_before = len(str(one.vmpool.monitoring(last_seconds=-1)))
    sleep(60)
    lines_after  = len(str(one.vmpool.monitoring(last_seconds=-1)))
    assert lines_before < lines_after
    