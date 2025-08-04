import pytest

from api                import One
from utils.kerberos     import PyoneWrap
from config.base        import API_URI, BrestAdmin


from tests._common_methods.chmod    import random_chmod__test, not_exist__test



# =================================================================================================
# TESTS
# =================================================================================================



def test_vm_not_exist(one: One):
    not_exist__test(one.vm)




def test_chmod(one: One, dummy_vm: int):
    vm_id = dummy_vm
    random_chmod__test(one.vm, vm_id)



# @pytest.mark.KERBEROS
# def test_chmod_KERBEROS(dummy_vm: int):
#     pw    = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#     one   = pw.get_client()
#     vm_id = dummy_vm
#     permissions = (1, 1, 1, 1, 1, 1, 1, 1, 1)

#     _id = one.vm.chmod(vm_id, *permissions, pw.sessionDir)
#     pw.run_one_vm_action()
#     assert _id == vm_id

#     new_vm_permissions = one.vm.info(vm_id, True).PERMISSIONS

#     assert new_vm_permissions.OWNER_U == 1
#     assert new_vm_permissions.OWNER_M == 1
#     assert new_vm_permissions.OWNER_A == 1

#     assert new_vm_permissions.GROUP_U == 1
#     assert new_vm_permissions.GROUP_M == 1
#     assert new_vm_permissions.GROUP_A == 1

#     assert new_vm_permissions.OTHER_U == 1
#     assert new_vm_permissions.OTHER_M == 1
#     assert new_vm_permissions.OTHER_A == 1
