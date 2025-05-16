import pytest
import random

from pyone          import OneException
from api            import One
from utils          import get_unic_name
from one_cli.vm     import vm_exist, VirtualMachine
from config         import ADMIN_NAME




# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_no_memory_in_template(one: One):
    with pytest.raises(OneException):
        one.vm.allocate("CPU=1")
    

@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_no_cpu_in_template(one: One):
    with pytest.raises(OneException):
        one.vm.allocate("MEMORY=1")


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_allocate_vm(one: One):
    name    = get_unic_name()
    cpu     = random.randint(1, 3)
    vcpu    = random.randint(1, 3)
    memory  = random.randint(1, 128)

    template = f"""
        NAME = {name}
        CPU = {cpu}
        VCPU = {vcpu}
        MEMORY = {memory}
    """
    _id = one.vm.allocate(template, False)

    assert vm_exist(_id)
    vm      = VirtualMachine(_id)
    vm_info = vm.info()
    assert vm_info.NAME == name
    assert vm_info.STATE != 2
    assert int(vm_info.TEMPLATE["CPU"])     == cpu
    assert int(vm_info.TEMPLATE["VCPU"])    == vcpu
    assert int(vm_info.TEMPLATE["MEMORY"])  == memory
    vm.terminate(True)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_allocate_vm_by_xml(one: One):
    name    = get_unic_name()
    cpu     = random.randint(1, 3)
    vcpu    = random.randint(1, 3)
    memory  = random.randint(1, 128)

    template = f"""
        <VM>
            <NAME>{name}</NAME>
            <CPU>{cpu}</CPU>
            <VCPU>{vcpu}</VCPU>
            <MEMORY>{memory}</MEMORY>
        </VM>
    """
    
    _id = one.vm.allocate(template.strip(), False)

    assert vm_exist(_id)
    vm      = VirtualMachine(_id)
    vm_info = vm.info()
    assert vm_info.NAME == name
    assert vm_info.STATE != 2
    assert int(vm_info.TEMPLATE["CPU"])     == cpu
    assert int(vm_info.TEMPLATE["VCPU"])    == vcpu
    assert int(vm_info.TEMPLATE["MEMORY"])  == memory
    vm.terminate(True)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_allocate_and_hold(one: One):
    _id = one.vm.allocate("CPU=1\nMEMORY=1", True)
    assert vm_exist(_id)
    vm = VirtualMachine(_id)
    assert vm.info().STATE == 2
    vm.terminate(True)
