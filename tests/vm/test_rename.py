import pytest

from api                import One
from config.tests       import INVALID_CHARS
from utils.other        import get_unic_name
from utils.kerberos     import PyoneWrap
from config.base        import API_URI, BrestAdmin


from tests._common_methods.rename   import rename__test
from tests._common_methods.rename   import not_exist__test
from tests._common_methods.rename   import cant_be_renamed__test










def test_vm_not_exist(one: One):
    not_exist__test(one.vm)


def test_rename(one: One, dummy_vm: int):
    vm_id = dummy_vm
    rename__test(one.vm, vm_id)


def test_empty_name(one: One, dummy_vm: int):
    vm_id = dummy_vm
    cant_be_renamed__test(one.vm, vm_id, "")


@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, dummy_vm: int, char: str):
    vm_id = dummy_vm
    cant_be_renamed__test(one.vm, vm_id, f"{char}")
    cant_be_renamed__test(one.vm, vm_id, f"Greg{char}")
    cant_be_renamed__test(one.vm, vm_id, f"{char}Vetkin")
    cant_be_renamed__test(one.vm, vm_id, f"Greg{char}Vetkin")



def test_rename_KERBEROS(dummy_vm: int):
    vm_id = dummy_vm
    new_name = get_unic_name()

    pw = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    _id = one.vm.rename(vm_id, new_name, pw.sessionDir)
    pw.run_one_vm_action()

    assert _id == vm_id
    assert new_name == one.vm.info(vm_id, True).NAME


