import pytest
import random
from pyone           import OneException
from time            import sleep
from api             import One
from utils           import get_unic_name
from one_cli.vm      import VirtualMachine
from config          import ADMIN_NAME



def await_vm_status_code(one: One, vm_id: int, status_code: int, intervals=1.0):
    while one.vm.info(vm_id).STATE != status_code:
        sleep(intervals)


@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def hold_vm(one: One): 
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=0.1\nMEMORY=1\n", hold_vm=True)
    await_vm_status_code(one, vm_id, 2)

    yield VirtualMachine(vm_id)

    one.vm.action("terminate-hard", vm_id)






# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(OneException):
        one.vm.deploy(99999, 0)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_not_exist(one: One, hold_vm: VirtualMachine):
    with pytest.raises(OneException):
        one.vm.deploy(hold_vm._id, 999999)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_deploy_on_host(one: One, hold_vm: VirtualMachine):
    host_ids_list   = [host.ID for host in one.hostpool.info().HOST]
    target_host_id  = random.choice(host_ids_list)

    _id = one.vm.deploy(hold_vm._id, target_host_id)
    assert _id == hold_vm._id

    sleep(5)
    
    assert hold_vm._id in one.host.info(target_host_id).VMS.ID

