import pytest
import random


from time               import sleep
from pyone              import OneException
from api                import One
from utils              import get_unic_name
from one_cli.vm         import VirtualMachine
from config             import ADMIN_NAME

from tests._common_tests.info import info__test


def await_vm_status_code(one: One, vm_id: int, status_code: int, intervals=1.0):
    while one.vm.info(vm_id).STATE != status_code:
        sleep(intervals)


@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def vm(one: One): 
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=0.1\nMEMORY=1\n")
    await_vm_status_code(one, vm_id, 8)

    yield VirtualMachine(vm_id)

    one.vm.action("terminate-hard", vm_id)
    await_vm_status_code(one, vm_id, 6)






# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(OneException):
        one.vm.info(99999)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_info(one: One, vm: VirtualMachine):
    vm_info = one.vm.info(vm._id, False)
    assert vm_info.ID == vm._id


@pytest.mark.skip(reason="No idea what to check")
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_decrypt_vm_info(one: One, vm: VirtualMachine):
    # TODO: Написать тест, когда будет понятно, что именно декриптится и как это проверить
    pass
