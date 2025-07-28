import pytest

from api                import One
from utils.kerberos     import PyoneWrap
from config.base        import API_URI, BrestAdmin

from tests._common_methods.chown    import object_not_exist__test
from tests._common_methods.chown    import user_not_exist__test
from tests._common_methods.chown    import group_not_exist__test
from tests._common_methods.chown    import user_and_group_change__test
from tests._common_methods.chown    import user_and_group_not_changed__test
from tests._common_methods.chown    import user_change__test
from tests._common_methods.chown    import group_change__test




# =================================================================================================
# TESTS
# =================================================================================================




def test_vm_not_exist(one: One):
    object_not_exist__test(one.vm)


def test_user_not_exist(one: One, dummy_vm: int):
    vm_id = dummy_vm
    user_not_exist__test(one.vm, vm_id)


def test_group_not_exist(one: One, dummy_vm: int):
    vm_id = dummy_vm
    group_not_exist__test(one.vm, vm_id)


def test_change_user_and_group(one: One, dummy_vm: int, dummy_user: int, dummy_group: int):
    vm_id = dummy_vm
    user_id = dummy_user
    group_id = dummy_group
    user_and_group_change__test(one.vm, vm_id, user_id, group_id)


def test_as_was_user_and_group(one: One, dummy_vm: int):
    vm_id = dummy_vm
    user_and_group_not_changed__test(one.vm, vm_id)



def test_change_user(one: One, dummy_vm: int, dummy_user: int):
    vm_id = dummy_vm
    user_id = dummy_user
    user_change__test(one.vm, vm_id, user_id)


def test_change_group(one: One, dummy_vm: int, dummy_group: int):
    vm_id = dummy_vm
    group_id = dummy_group
    group_change__test(one.vm, vm_id, group_id)


@pytest.mark.KERBEROS
def test_chown_KERBEROS(dummy_vm: int, dummy_user: int, dummy_group: int):
    vm_id = dummy_vm
    user_id = dummy_user
    group_id = dummy_group

    pw = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    _id = one.vm.chown(vm_id, user_id, group_id, pw.sessionDir)
    pw.run_one_vm_action()
    assert _id == vm_id

    vm_info = one.vm.info(vm_id, True)
    assert user_id  == vm_info.UID
    assert group_id == vm_info.GID
