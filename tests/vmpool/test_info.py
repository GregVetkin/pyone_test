import pytest
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


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_show_all_vms(one: One, vms: List[VirtualMachine]):
    created_vm_ids  = [vm._id for vm in vms]
    vmpool          = one.vmpool.info().VM
    vmpool_ids      = [vm.ID for vm in vmpool]
    
    assert set(created_vm_ids).issubset(vmpool_ids)
