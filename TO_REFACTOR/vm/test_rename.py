import pytest

from api                        import One
from one_cli.vm                 import VirtualMachine, create_vm
from config                     import ADMIN_NAME, BAD_SYMBOLS

from tests._common_tests.rename import rename__test
from tests._common_tests.rename import rename_if_not_exist__test
from tests._common_tests.rename import cant_be_renamed__test




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
    rename_if_not_exist__test(one.vm)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_rename_vm(one: One, vm: VirtualMachine):
    rename__test(one.vm, vm)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_empty_host_name(one: One, vm: VirtualMachine):
    cant_be_renamed__test(one.vm, vm, "")


@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unavailable_symbols_in_vm_name(one: One, vm: VirtualMachine, bad_symbol: str):
    cant_be_renamed__test(one.vm, vm, f"{bad_symbol}")
    cant_be_renamed__test(one.vm, vm, f"Greg{bad_symbol}")
    cant_be_renamed__test(one.vm, vm, f"{bad_symbol}Vetkin")
    cant_be_renamed__test(one.vm, vm, f"Greg{bad_symbol}Vetkin")

