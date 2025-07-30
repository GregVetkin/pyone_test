import pytest
import random
import pyone

from api                import One

from utils.kerberos     import PyoneWrap
from utils.other        import wait_until

from config.base        import API_URI, BrestAdmin
from config.opennebula  import VmStates





@pytest.fixture
def dummy_vm_poweroff(one: One, dummy_vm: int):
    vm_id = dummy_vm
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF)
    return vm_id




# =================================================================================================
# TESTS
# =================================================================================================



def test_vm_not_exist(one: One):
    vm_id  = random.randint(9999, 999999)
    nic_id = 0

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.detachnic(vm_id, nic_id)



def test_vnet_not_exist(one: One, dummy_vm_poweroff: int):
    vm_id  = dummy_vm_poweroff
    nic_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneActionException):
        one.vm.detachnic(vm_id, nic_id)



def test_detachnic(one: One, poweroff_vm_mini: int):
    vm_id   = poweroff_vm_mini
    vm_info = one.vm.info(vm_id, False)
    vm_nics = vm_info.TEMPLATE["NIC"]

    if isinstance(vm_nics, dict):
        nic_count_before = 1
        nic_id = int(vm_nics["NIC_ID"])

    elif isinstance(vm_nics, list):
        nic_count_before = len(vm_nics)
        nic_id = max(vm_nics, key=lambda nic: int(nic["NIC_ID"]))

    else:
        raise "ВМ без сетей"
    
    
    _id = one.vm.detachnic(vm_id, nic_id)
    assert _id == vm_id

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    vm_info = one.vm.info(vm_id, False)
    vm_template = vm_info.TEMPLATE

    if "NIC" not in vm_template:
        nic_count_after = 0

    elif isinstance(vm_template["NIC"], dict):
        nic_count_after = 1
        
    else:
        nic_count_after = len(vm_template["NIC"])

    assert nic_count_after - nic_count_before == -1

    if nic_count_after > 1:
        assert nic_id not in [int(nic["NIC_ID"] for nic in vm_template["NIC"])]
    
    if nic_count_after == 1:
        assert nic_id != int(vm_template["NIC"]["NIC_ID"])


@pytest.mark.KERBEROS
def test_detachnic_KERBEROS(poweroff_vm_mini: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id   = poweroff_vm_mini
    vm_info = one.vm.info(vm_id, False)
    vm_nics = vm_info.TEMPLATE["NIC"]

    if isinstance(vm_nics, dict):
        nic_count_before = 1
        nic_id = int(vm_nics["NIC_ID"])

    elif isinstance(vm_nics, list):
        nic_count_before = len(vm_nics)
        nic_id = max(vm_nics, key=lambda nic: int(nic["NIC_ID"]))

    else:
        raise "ВМ без сетей"
    
    
    _id = one.vm.detachnic(vm_id, nic_id, pw.sessionDir)
    pw.run_one_vm_action()
    assert _id == vm_id

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    vm_info = one.vm.info(vm_id, False)
    vm_template = vm_info.TEMPLATE

    if "NIC" not in vm_template:
        nic_count_after = 0

    elif isinstance(vm_template["NIC"], dict):
        nic_count_after = 1
        
    else:
        nic_count_after = len(vm_template["NIC"])

    assert nic_count_after - nic_count_before == -1

    if nic_count_after > 1:
        assert nic_id not in [int(nic["NIC_ID"] for nic in vm_template["NIC"])]
    
    if nic_count_after == 1:
        assert nic_id != int(vm_template["NIC"]["NIC_ID"])



