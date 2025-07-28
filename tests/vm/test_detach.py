import pytest
import random

from pyone              import OneNoExistsException, OneActionException
from api                import One

from utils.commands     import run_command_via_ssh, check_ping
from utils.connection   import brest_admin_ssh_conn, local_admin_ssh_conn
from utils.kerberos     import PyoneWrap
from utils.other        import wait_until, get_unic_name
from utils.version      import Version

from config.base        import API_URI, BrestAdmin, BREST_VERSION
from config.opennebula  import VmStates, VmLcmStates, VmRecoverOperations, VmActions





@pytest.fixture
def poweroff_vm(one: One):
    if Version(BREST_VERSION) < Version("4"):
        script_dir = "~/brest"
        ssh_conn   = local_admin_ssh_conn
    else:
        script_dir = "/opt/brest"
        ssh_conn   = brest_admin_ssh_conn
    
    vm_name = f"api_test_{random.randint(0, 9999)}" # С длинным именем из get_unic_name(), cli_prepare.sh не отрабатывает отлов статуса ВМ
    command = f"cd {script_dir} && ./cli_prepare.sh create_vm mini {vm_name} nonpers"
    
    run_command_via_ssh(ssh_conn, command)
    vm_id = next(vm.ID for vm in one.vmpool.info().VM if vm.NAME == vm_name)

    yield vm_id

    if one.vm.info(vm_id).STATE != VmStates.DONE:
        run_command_via_ssh(brest_admin_ssh_conn, f"onevm terminate {vm_id} --hard")



@pytest.fixture
def dummy_vm_poweroff(one: One, dummy_vm: int):
    vm_id = dummy_vm
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF)
    return vm_id




# =================================================================================================
# TESTS
# =================================================================================================



def test_vm_not_exist(one: One):
    vm_id = 99999
    disk_id = 0
    with pytest.raises(OneNoExistsException):
        one.vm.detach(vm_id, disk_id)



def test_disk_not_exist(one: One, dummy_vm_poweroff: int):
    vm_id = dummy_vm_poweroff
    disk_id = 999999
    with pytest.raises(OneActionException):
        one.vm.detach(vm_id, disk_id)



def test_detach(one: One, poweroff_vm: int):
    vm_id = poweroff_vm
    vm_info = one.vm.info(vm_id, True)
    vm_disks = vm_info.TEMPLATE["DISK"]

    if isinstance(vm_disks, dict):
        disk_count_before = 1
        disk_id = int(vm_disks["DISK_ID"])

    elif isinstance(vm_disks, list):
        disk_count_before = len(vm_disks)
        disk_id = max(vm_disks, key=lambda disk: int(disk["DISK_ID"]))

    else:
        raise "ВМ без дисков"
    
    
    _id = one.vm.detach(vm_id, disk_id)
    assert _id == vm_id

    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF)

    vm_info = one.vm.info(vm_id, True)
    vm_template = vm_info.TEMPLATE

    if "DISK" not in vm_template:
        disk_count_after = 0

    elif isinstance(vm_template["DISK"], dict):
        disk_count_after = 1
        
    else:
        disk_count_after = len(vm_template["DISK"])

    assert disk_count_after - disk_count_before == -1

    if disk_count_after > 1:
        assert disk_id not in [int(disk["DISK_ID"] for disk in vm_template["DISK"])]
    
    if disk_count_after == 1:
        assert disk_id != int(vm_template["DISK"]["DISK_ID"])



@pytest.mark.KERBEROS
def test_detach_KERBEROS(poweroff_vm: int):
    pw = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
    one = pw.get_client()
    vm_id = poweroff_vm
    vm_info = one.vm.info(vm_id, True)
    vm_disks = vm_info.TEMPLATE["DISK"]

    if isinstance(vm_disks, dict):
        disk_count_before = 1
        disk_id = int(vm_disks["DISK_ID"])

    elif isinstance(vm_disks, list):
        disk_count_before = len(vm_disks)
        disk_id = max(vm_disks, key=lambda disk: int(disk["DISK_ID"]))

    else:
        raise "ВМ без дисков"
    
    
    _id = one.vm.detach(vm_id, disk_id, pw.sessionDir)
    pw.run_one_vm_action()
    assert _id == vm_id

    wait_until(lambda: one.vm.info(vm_id, True).STATE == VmStates.POWEROFF)

    vm_info = one.vm.info(vm_id, True)
    vm_template = vm_info.TEMPLATE

    if "DISK" not in vm_template:
        disk_count_after = 0

    elif isinstance(vm_template["DISK"], dict):
        disk_count_after = 1

    else:
        disk_count_after = len(vm_template["DISK"])

    assert disk_count_after - disk_count_before == -1

    if disk_count_after > 1:
        assert disk_id not in [int(disk["DISK_ID"] for disk in vm_template["DISK"])]
    
    if disk_count_after == 1:
        assert disk_id != int(vm_template["DISK"]["DISK_ID"])
