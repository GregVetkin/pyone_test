import pytest

from api                import One
from utils              import get_unic_name
from one_cli.vm         import VirtualMachine, create_vm
from one_cli.user       import User, create_user
from one_cli.group      import Group, create_group
from config             import ADMIN_NAME

from tests._common_tests.chown  import chown_object_not_exist__test
from tests._common_tests.chown  import chown_user_not_exist__test
from tests._common_tests.chown  import chown_group_not_exist__test
from tests._common_tests.chown  import chown_user_and_group_change__test
from tests._common_tests.chown  import chown_user_and_group_not_changed__test




@pytest.fixture
def vm():
    vm_id = create_vm("CPU=1\nMEMORY=1", await_vm_offline=False)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()
    
    
    
@pytest.fixture
def user():
    user_id = create_user(get_unic_name())
    user    = User(user_id)
    yield user
    user.delete()


@pytest.fixture
def group():
    group_id = create_group(get_unic_name())
    group    = Group(group_id)
    yield group
    group.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    chown_object_not_exist__test(one.vm)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_user_not_exist(one: One, vm: VirtualMachine):
    chown_user_not_exist__test(one.vm, vm)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_group_not_exist(one: One, vm: VirtualMachine):
    chown_group_not_exist__test(one.vm, vm)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_user_and_group_change(one: One, vm: VirtualMachine, user: User, group: Group):
    chown_user_and_group_change__test(one.vm, vm, user, group)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_user_and_group_not_changed(one: One, vm: VirtualMachine):
    chown_user_and_group_not_changed__test(one.vm, vm)



