import pytest
import random

from pyone              import OneActionException
from api                import One
from utils.other        import get_unic_name, wait_until
from config.opennebula  import VmStates, VmRecoverOperations




# =================================================================================================
# TESTS
# =================================================================================================



def test_memory_mandatory(one: One):
    with pytest.raises(OneActionException):
        one.vm.allocate("CPU=1")
    

def test_cpu_mandatory(one: One):
    with pytest.raises(OneActionException):
        one.vm.allocate("MEMORY=1")


def test_hold(one: One):
    template = "CPU=1\nMEMORY=1" 
    hold_vm  = True
    vm_id    = one.vm.allocate(template, hold_vm)
    assert one.vm.info(vm_id).STATE == VmStates.HOLD



def test_allocate_vm(one: One):
    name    = get_unic_name()
    cpu     = random.randint(1, 3)
    vcpu    = random.randint(1, 3)
    memory  = random.randint(1, 128)

    template = f"""
        NAME    = {name}
        CPU     = {cpu}
        VCPU    = {vcpu}
        MEMORY  = {memory}
    """
    vm_id   = one.vm.allocate(template, False)
    vm_info = one.vm.info(vm_id)

    assert vm_info.NAME == name
    assert int(vm_info.TEMPLATE["CPU"])     == cpu
    assert int(vm_info.TEMPLATE["VCPU"])    == vcpu
    assert int(vm_info.TEMPLATE["MEMORY"])  == memory

    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF)
    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.DONE)




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
    vm_id   = one.vm.allocate(template, False)
    vm_info = one.vm.info(vm_id)

    assert vm_info.NAME == name
    assert int(vm_info.TEMPLATE["CPU"])     == cpu
    assert int(vm_info.TEMPLATE["VCPU"])    == vcpu
    assert int(vm_info.TEMPLATE["MEMORY"])  == memory

    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF)
    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.DONE)




