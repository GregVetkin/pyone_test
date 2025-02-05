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



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vms_except_done(one: One, vms: List[VirtualMachine]):
    vmpool = one.vmpool.info(vm_state_filter=-1).VM
    
    for vm in vmpool:
        assert vm.STATE != 6



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_start_id_filter(one: One, vms: List[VirtualMachine]):
    created_vm_ids  = [vm._id for vm in vms]
    filter_start_id = created_vm_ids[2]
    vmpool          = one.vmpool.info(start_id=filter_start_id).VM

    for vm in vmpool:
        assert vm.ID >= filter_start_id
    


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_end_id_filter(one: One, vms: List[VirtualMachine]):
    created_vm_ids  = [vm._id for vm in vms]
    filter_end_id   = created_vm_ids[4]
    vmpool          = one.vmpool.info(end_id=filter_end_id).VM

    for vm in vmpool:
        assert vm.ID <= filter_end_id



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_range_id_filter(one: One, vms: List[VirtualMachine]):
    created_vm_ids  = [vm._id for vm in vms]
    filter_start_id = created_vm_ids[2]
    filter_end_id   = created_vm_ids[4]
    vmpool          = one.vmpool.info(start_id=filter_start_id, end_id=filter_end_id).VM

    for vm in vmpool:
        assert vm.ID >= filter_start_id and vm.ID <= filter_end_id




