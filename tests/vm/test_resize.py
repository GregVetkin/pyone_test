import pytest
import random

from api                import One
from one_cli.vm         import VirtualMachine, create_vm
from config             import ADMIN_NAME
from pyone              import OneException



@pytest.fixture(scope="module")
def vm():
    vm_id = create_vm("CPU=1\nMEMORY=1\nVCPU=1", await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()
    




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(OneException):
        one.vm.resize(99999, "", False)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_resize(one: One, vm: VirtualMachine):
    new_cpu     = round(random.uniform(2.0, 4.0), 2)
    new_vcpu    = random.randint(2, 4)
    new_memory  = random.randint(16, 128)

    template = f"""
        CPU     = {new_cpu}
        VCPU    = {new_vcpu}
        MEMORY  = {new_memory}
    """

    _id = one.vm.resize(vm._id, template, False)
    assert _id == vm._id

    vm_new_template = one.vm.info(vm._id).TEMPLATE
    assert float(vm_new_template["CPU"])    == new_cpu
    assert int(vm_new_template["VCPU"])     == new_vcpu
    assert int(vm_new_template["MEMORY"])   == new_memory



@pytest.mark.parametrize("check_capacity", [True, False])
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_resize_check_over_host_capacity(one: One, vm: VirtualMachine, check_capacity: bool):
    vm_id = vm._id
    target_cpu_count = 999
    target_mem_count = 9999999999

    if check_capacity:
        with pytest.raises(OneException):
            one.vm.resize(vm_id, f"CPU={target_cpu_count}", check_capacity)

        with pytest.raises(OneException):
            one.vm.resize(vm_id, f"MEMORY={target_mem_count}", check_capacity)

    else:
        _id = one.vm.resize(vm_id, f"CPU={target_cpu_count}", check_capacity)
        assert _id == vm_id
        _id = one.vm.resize(vm_id, f"MEMORY={target_mem_count}", check_capacity)
        assert _id == vm_id