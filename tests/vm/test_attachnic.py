import pytest
import pyone
import random


from api                import One
from utils.other        import wait_until, get_unic_name
from utils.kerberos     import PyoneWrap
from config.opennebula  import VmStates
from config.base        import API_URI, BrestAdmin



@pytest.fixture
def dummy_vm_poweroff(one: One, dummy_vm: int):
    vm_id = dummy_vm
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    return vm_id


@pytest.fixture
def vnet(one: One):
    template = f"""
        NAME   = {get_unic_name()}
        VN_MAD = bridge
        AR = [ 
            TYPE = IP4,
            IP   = 1.1.1.1,
            SIZE = 1
        ]
    """
    vnet_id = one.vn.allocate(template, -1)
    yield vnet_id
    one.vn.delete(vnet_id)


# =================================================================================================
# TESTS
# =================================================================================================



def test_vm_not_exist(one: One, dummy_vnet: int):
    vm_id    = random.randint(9999, 999999)
    vnet_id  = dummy_vnet
    template = f"NIC=[NETWORK_ID={vnet_id}]"

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.attachnic(vm_id, template)



def test_vnet_not_exist(one: One, dummy_vm_poweroff: int):
    vm_id    = dummy_vm_poweroff
    vnet_id  = random.randint(9999, 999999)
    template = f"NIC=[NETWORK_ID={vnet_id}]"

    with pytest.raises(pyone.OneException):
        one.vm.attachnic(vm_id, template)


def test_vnet_with_no_AR(one: One, dummy_vm_poweroff: int,  dummy_vnet: int):
    vm_id    = dummy_vm_poweroff
    vnet_id  = dummy_vnet
    template = f"NIC=[NETWORK_ID={vnet_id}]"

    with pytest.raises(pyone.OneActionException):
        one.vm.attachnic(vm_id, template)




def test_attachnic(one: One, dummy_vm_poweroff: int, vnet: int):
    vm_id    = dummy_vm_poweroff
    vnet_id  = vnet
    template = f"NIC=[NETWORK_ID={vnet_id}]"

    vm_template_before = one.vm.info(vm_id, False).TEMPLATE

    if "NIC" not in vm_template_before:
        nic_count_brefore = 0
    elif isinstance(vm_template_before["NIC"], dict):
        nic_count_brefore = 1
    else:
        nic_count_brefore = len(vm_template_before["NIC"])


    _id = one.vm.attachnic(vm_id, template)
    assert _id == vm_id
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)


    vm_template = one.vm.info(vm_id, False).TEMPLATE
    vm_nics = vm_template["NIC"]


    if isinstance(vm_nics, dict):
        nic_count_after = 1
        added_nic = vm_nics
    else:
        nic_count_after = len(vm_nics)
        added_nic = max(vm_nics, key=lambda nic: int(nic["NIC_ID"]))

    assert nic_count_after - nic_count_brefore == 1
    assert int(added_nic["NETWORK_ID"]) == vnet_id

    one.vm.detachnic(vm_id, int(added_nic["NIC_ID"]))
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)




@pytest.mark.KERBEROS
def test_attachnic_KERBEROS(one: One, dummy_vm_poweroff: int, vnet: int):
    pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()

    vm_id    = dummy_vm_poweroff
    vnet_id  = vnet
    template = f"NIC=[NETWORK_ID={vnet_id}]"

    vm_template_before = one.vm.info(vm_id, False).TEMPLATE

    if "NIC" not in vm_template_before:
        nic_count_brefore = 0
    elif isinstance(vm_template_before["NIC"], dict):
        nic_count_brefore = 1
    else:
        nic_count_brefore = len(vm_template_before["NIC"])


    _id = one.vm.attachnic(vm_id, template, pw.sessionDir)
    pw.run_one_vm_action()
    assert _id == vm_id
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)


    vm_template = one.vm.info(vm_id, False).TEMPLATE
    vm_nics = vm_template["NIC"]


    if isinstance(vm_nics, dict):
        nic_count_after = 1
        added_nic = vm_nics
    else:
        nic_count_after = len(vm_nics)
        added_nic = max(vm_nics, key=lambda nic: int(nic["NIC_ID"]))

    assert nic_count_after - nic_count_brefore == 1
    assert int(added_nic["NETWORK_ID"]) == vnet_id

    one.vm.detachnic(vm_id, int(added_nic["NIC_ID"]))
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

