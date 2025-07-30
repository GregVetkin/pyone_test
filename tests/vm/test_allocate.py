import pytest
import pyone
import random

from api                import One
from utils.other        import get_unic_name, wait_until
from utils.kerberos     import PyoneWrap
from config.opennebula  import VmStates, VmRecoverOperations
from config.base        import API_URI, BrestAdmin



# =================================================================================================
# TESTS
# =================================================================================================



def test_memory_mandatory(one: One):
    template = "CPU=0.1"
    hold_vm  = False

    with pytest.raises(pyone.OneException):
        one.vm.allocate(template, hold_vm)
    


def test_cpu_mandatory(one: One):
    template = "MEMORY=32"
    hold_vm  = False

    with pytest.raises(pyone.OneException):
        one.vm.allocate(template, hold_vm)



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
    vm_info = one.vm.info(vm_id, False)

    assert vm_info.NAME == name
    assert int(vm_info.TEMPLATE["CPU"])     == cpu
    assert int(vm_info.TEMPLATE["VCPU"])    == vcpu
    assert int(vm_info.TEMPLATE["MEMORY"])  == memory

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.DONE)




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
    </VM>"""
    template = template.strip()
    vm_id   = one.vm.allocate(template, False)
    vm_info = one.vm.info(vm_id, False)

    assert vm_info.NAME == name
    assert int(vm_info.TEMPLATE["CPU"])     == cpu
    assert int(vm_info.TEMPLATE["VCPU"])    == vcpu
    assert int(vm_info.TEMPLATE["MEMORY"])  == memory

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.DONE)



@pytest.mark.parametrize("hold_vm", [True, False])
def test_hold(one: One, hold_vm: bool):
    template = "CPU=1\nMEMORY=1"
    vm_id    = one.vm.allocate(template, hold_vm)
    vm_state = one.vm.info(vm_id, False).STATE

    if hold_vm:
        assert vm_state == VmStates.HOLD
    else:
        assert vm_state == VmStates.PENDING

    one.vm.recover(vm_id, VmRecoverOperations.DELETE)



@pytest.mark.KERBEROS
def test_allocate_vm_KERBEROS():
    pw      = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one     = pw.get_client()
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
    vm_id   = one.vm.allocate(template, False, pw.sessionDir)
    pw.run_one_vm_action()

    vm_info = one.vm.info(vm_id, False)

    assert vm_info.NAME == name
    assert int(vm_info.TEMPLATE["CPU"])     == cpu
    assert int(vm_info.TEMPLATE["VCPU"])    == vcpu
    assert int(vm_info.TEMPLATE["MEMORY"])  == memory

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.DONE)