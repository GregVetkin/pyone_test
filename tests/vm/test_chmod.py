import pytest

from api                        import One
from one_cli.vm                 import VirtualMachine, create_vm
from config                     import ADMIN_NAME

from tests._common_tests.chmod  import chmod__test
from tests._common_tests.chmod  import chmod_if_not_exist__test
from tests._common_tests.chmod  import _rights_tuples_list





@pytest.fixture(scope="module")
def vm():
    vm_id = create_vm("CPU=1\nMEMORY=1", await_vm_offline=False)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    chmod_if_not_exist__test(one.vm)



@pytest.mark.parametrize("rights", _rights_tuples_list())
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_change_vm_rights(one: One, vm: VirtualMachine, rights):
    chmod__test(one.vm, vm, rights)

