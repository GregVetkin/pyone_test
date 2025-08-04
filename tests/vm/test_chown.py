import pytest
import pyone
import random

from api                import One
from utils.kerberos     import PyoneWrap
from config.base        import API_URI, BrestAdmin


from tests._common_methods.chown    import not_exist__test, chown__test







def test_vm_not_exist(one: One):
    not_exist__test(one.vm)


def test_user_not_exist(one: One, dummy_vm: int):
    vm_id    = dummy_vm
    user_id  = random.randint(9999, 999999)
    group_id = -1

    with pytest.raises(pyone.OneNoExistsException):
        chown__test(one.vm, vm_id, user_id, group_id)


def test_group_not_exist(one: One, dummy_vm: int):
    vm_id    = dummy_vm
    user_id  = -1
    group_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneNoExistsException):
        chown__test(one.vm, vm_id, user_id, group_id)


def test_user_and_group_change(one: One, dummy_vm: int, dummy_user: int, dummy_group: int):
    vm_id    = dummy_vm
    user_id  = dummy_user
    group_id = dummy_group
    chown__test(one.vm, vm_id, user_id, group_id)


def test_user_and_group_not_changed(one: One, dummy_vm: int):
    vm_id    = dummy_vm
    user_id  = -1
    group_id = -1
    chown__test(one.vm, vm_id, user_id, group_id)



def test_only_user_change(one: One, dummy_vm: int, dummy_user: int):
    vm_id    = dummy_vm
    user_id  = dummy_user
    group_id = -1
    chown__test(one.vm, vm_id, user_id, group_id)


def test_only_group_change(one: One, dummy_vm: int, dummy_group: int):
    vm_id    = dummy_vm
    user_id  = -1
    group_id = dummy_group
    chown__test(one.vm, vm_id, user_id, group_id)




# @pytest.mark.KERBEROS
# def test_chown_KERBEROS(dummy_vm: int, dummy_user: int, dummy_group: int):
#     vm_id    = dummy_vm
#     user_id  = dummy_user
#     group_id = dummy_group

#     pw = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#     one = pw.get_client()

#     _id = one.vm.chown(vm_id, user_id, group_id, pw.sessionDir)
#     pw.run_one_vm_action()
#     assert _id == vm_id

#     vm_info = one.vm.info(vm_id, False)
#     assert user_id  == vm_info.UID
#     assert group_id == vm_info.GID
