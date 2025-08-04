import pytest
import pyone

from api                import One
from utils.other        import get_unic_name
from config.tests       import INVALID_CHARS

from tests._common_methods.rename   import rename__test, not_exist__test











def test_vm_not_exist(one: One):
    not_exist__test(one.vm)


def test_rename(one: One, dummy_vm: int):
    vm_id    = dummy_vm
    new_name = get_unic_name()

    rename__test(one.vm, vm_id, new_name)


def test_empty_name(one: One, dummy_vm: int):
    vm_id    = dummy_vm
    new_name = ""
    
    with pytest.raises(pyone.OneActionException):
        rename__test(one.vm, vm_id, new_name)



@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_vm: int, char: str):
    vm_id = dummy_vm

    with pytest.raises(pyone.OneActionException):
        rename__test(one.vm, vm_id, f"{char}")
        
    with pytest.raises(pyone.OneActionException):
        rename__test(one.vm, vm_id, f"Greg{char}")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.vm, vm_id, f"{char}Vetkin")

    with pytest.raises(pyone.OneActionException):
        rename__test(one.vm, vm_id, f"Greg{char}Vetkin")




# def test_rename_KERBEROS(dummy_vm: int):
#     vm_id = dummy_vm
#     new_name = get_unic_name()

#     pw = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#     one = pw.get_client()

#     _id = one.vm.rename(vm_id, new_name, pw.sessionDir)
#     pw.run_one_vm_action()

#     assert _id == vm_id
#     assert new_name == one.vm.info(vm_id, True).NAME


