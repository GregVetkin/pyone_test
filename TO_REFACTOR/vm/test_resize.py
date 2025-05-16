import pytest
import random
import pyone
import time

from api                import One
from one_cli.vm         import VirtualMachine, create_vm
from config             import ADMIN_NAME, API_URI
from pyone              import OneException
from utils              import run_command


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
    time.sleep(3)
    vm_new_template = one.vm.info(vm._id).TEMPLATE
    assert float(vm_new_template["CPU"])    == new_cpu
    assert int(vm_new_template["VCPU"])     == new_vcpu
    assert int(vm_new_template["MEMORY"])   == new_memory




@pytest.mark.parametrize("enforce", [True, False])
def test_oneadmin_enforce_host_capacity(vm: VirtualMachine, enforce: bool):
    oneadmin_auth = run_command("sudo oneuser login oneadmin")
    one = One(pyone.OneServer(API_URI, oneadmin_auth))
    time.sleep(3)
    vm_id = vm._id
    target_cpu_count = 999
    target_mem_count = 9999999999

    if enforce:
        _id = one.vm.resize(vm_id, f"CPU={target_cpu_count}", enforce)
        assert _id == vm_id
        time.sleep(1)
        _id = one.vm.resize(vm_id, f"MEMORY={target_mem_count}", enforce)
        assert _id == vm_id
        time.sleep(1)
        vm_new_template = one.vm.info(vm_id).TEMPLATE
        assert float(vm_new_template["CPU"]) == target_cpu_count
        assert int(vm_new_template["MEMORY"])== target_mem_count

    else:
        with pytest.raises(OneException):
            one.vm.resize(vm_id, f"CPU={target_cpu_count}", enforce)
        with pytest.raises(OneException):
            one.vm.resize(vm_id, f"MEMORY={target_mem_count}", enforce)
