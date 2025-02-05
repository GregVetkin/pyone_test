import pytest
import random
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
def test_not_existed_ids(one: One):
    vms_infoset = one.vmpool.infoset("999999,999998,999997", False).VM
    assert len(vms_infoset) == 0




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_id_list(one: One, vms: List[VirtualMachine]):
    created_vm_ids  = [vm._id for vm in vms]
    random_ids      = random.sample(created_vm_ids, random.randint(1, len(created_vm_ids)))
    ids_string      = ",".join([str(_id) for _id in random_ids])
    vms_infoset     = one.vmpool.infoset(ids_string, False).VM

    assert len(random_ids) == len(vms_infoset)

    for vm in vms_infoset:
        assert vm.ID in random_ids



@pytest.mark.parametrize("extended", [True, False])
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_extended_data(one: One, vms: List[VirtualMachine], extended: bool):
    attribute_name  = "TEST_ATTR"
    created_vm_ids  = [vm._id for vm in vms]
    random_ids      = random.sample(created_vm_ids, random.randint(1, len(created_vm_ids)))
    ids_string      = ",".join([str(_id) for _id in random_ids])

    for _id in random_ids:
        one.vm.update(_id, f"{attribute_name}=test_value", False)

    vms_infoset = one.vmpool.infoset(ids_string, extended).VM

    for vm in vms_infoset:
        if extended:
            assert vm.USER_TEMPLATE.get(attribute_name)
        else:
            assert not vm.USER_TEMPLATE.get(attribute_name)
