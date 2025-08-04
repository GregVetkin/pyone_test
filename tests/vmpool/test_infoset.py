import pytest
import random
from typing             import List
from api                import One
from utils.other        import get_unic_name
from config.opennebula  import VmStates, VmRecoverOperations





@pytest.fixture
def vms(one: One):
    vms_list = []

    for _ in range(5):
        vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=0.1\nMEMORY=1\n", False)
        vms_list.append(vm_id)

    yield vms_list

    for vm in vms_list:
        one.vm.recover(vm, VmRecoverOperations.DELETE)





# =================================================================================================
# TESTS
# =================================================================================================



def test_not_existed_ids(one: One):
    vm_set   = "999999,999998,999997"
    extended = False

    vm_pool = one.vmpool.infoset(vm_set, extended).VM
    assert len(vm_pool) == 0




def test_id_list(one: One, vms: List[int]):
    created_vm_ids  = vms
    random_ids      = random.sample(created_vm_ids, random.randint(1, len(created_vm_ids)))
    ids_string      = ",".join([str(_id) for _id in random_ids])
    extended        = False

    vm_pool = one.vmpool.infoset(ids_string, extended).VM

    assert len(random_ids) == len(vm_pool)

    for vm in vm_pool:
        assert vm.ID in random_ids




@pytest.mark.parametrize("extended", [True, False])
def test_extended_data(one: One, vms: List[int], extended: bool):
    created_vm_ids  = vms
    attribute_name  = "TEST_ATTR"
    random_ids      = random.sample(created_vm_ids, random.randint(1, len(created_vm_ids)))
    ids_string      = ",".join([str(_id) for _id in random_ids])

    for _id in random_ids:
        one.vm.update(_id, f"{attribute_name}=test_value", 1)

    vms_infoset = one.vmpool.infoset(ids_string, extended).VM

    for vm in vms_infoset:
        if extended:
            assert attribute_name in vm.USER_TEMPLATE
        else:
            assert attribute_name not in vm.USER_TEMPLATE
