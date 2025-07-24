import pytest
import random
import pyone
import time

from utils.commands     import run_command_via_ssh
from utils.connection   import brest_admin_ssh_conn, local_admin_ssh_conn
from config.base        import API_URI, BrestAdmin, BREST_VERSION
from config.opennebula  import VmStates, VmLcmStates
from utils.aic          import PyoneWrap
from utils.other        import wait_until, get_unic_name
from utils.version      import Version
from pyone              import OneNoExistsException
from pyone              import OneActionException
from api                import One




@pytest.fixture
def poweroff_vm(one: One):
    if Version(BREST_VERSION) < Version("4"):
        script_dir = "~/brest"
        ssh_conn   = local_admin_ssh_conn
    else:
        script_dir = "/opt/brest"
        ssh_conn   = brest_admin_ssh_conn
    
    vm_name = "api_test" # С длинным именем из get_unic_name(), cli_prepare.sh не отрабатывает отлов статуса ВМ
    run_command_via_ssh(ssh_conn, f"cd {script_dir} && ./cli_prepare.sh create_vm mini {vm_name} nonpers")
    vm_id = next(vm.ID for vm in one.vmpool.info().VM if vm.NAME == vm_name)

    yield vm_id

    if one.vm.info(vm_id).STATE != VmStates.DONE:
        run_command_via_ssh(brest_admin_ssh_conn, f"onevm terminate {vm_id} --hard")


    

@pytest.fixture
def running_vm(one: One, poweroff_vm: int):
    vm_id = poweroff_vm
    run_command_via_ssh(brest_admin_ssh_conn, f"echo '{BrestAdmin.PASSWORD}' | kinit; onevm resume {vm_id}")
    wait_until(lambda: one.vm.info(vm_id).LCM_STATE == VmLcmStates.RUNNING)
    yield vm_id



# =================================================================================================
# TESTS
# =================================================================================================


def test_vm_not_exist(one: One):
    action = "terminate"
    vm_id  = 99999

    with pytest.raises(OneNoExistsException):
        one.vm.action(action, vm_id)


def test_action_not_exist(one: One, dummy_vm: int):
    action = "spamspamspam"
    vm_id  = dummy_vm

    with pytest.raises(OneActionException):
        one.vm.action(action, vm_id)





@pytest.mark.parametrize('action', ["terminate", "terminate-hard"])
class TestTerminate:
    def test_terminate(self, one: One, poweroff_vm: int, action: str):
        vm_id = poweroff_vm
        _id   = one.vm.action(action, vm_id)
        assert _id == vm_id

        wait_until(
            lambda: one.vm.info(vm_id).STATE == VmStates.DONE,
            timeout_message=f"ВМ {vm_id} не была удалена"
        )
        
    @pytest.mark.KERBEROS
    def test_terminate_KERBEROS(self, poweroff_vm: int, action: str):
        vm_id   = poweroff_vm
        pw      = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
        one     = pw.get_client()
        _id     = one.vm.action(action, vm_id, pw.sessionDir)
        pw.run_one_vm_action()

        assert _id == vm_id

        wait_until(
            lambda: one.vm.info(vm_id).STATE == VmStates.DONE,
            timeout_message=f"ВМ {vm_id} не была удалена"
        )



@pytest.mark.parametrize('action', ["undeploy", "undeploy-hard"])
class TestUndeploy:
    def test_undeploy(self, one: One, poweroff_vm: int, action: str):
        vm_id = poweroff_vm
        _id   = one.vm.action(action, vm_id)
        assert _id == vm_id

        wait_until(
            lambda: one.vm.info(vm_id).STATE == VmStates.UNDEPLOYED,
            timeout_message=f"ВМ {vm_id} не получила статус 'Неразвернута'"
        )

    @pytest.mark.KERBEROS    
    def test_undeploy_KERBEROS(self, poweroff_vm: int, action: str):
        vm_id   = poweroff_vm
        pw      = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
        one     = pw.get_client()
        _id     = one.vm.action(action, vm_id, pw.sessionDir)
        pw.run_one_vm_action()

        assert _id == vm_id

        wait_until(
            lambda: one.vm.info(vm_id).STATE == VmStates.UNDEPLOYED,
            timeout_message=f"ВМ {vm_id} не получила статус 'Неразвернута'"
        )




@pytest.mark.parametrize('action', ["poweroff", "poweroff-hard"])
class TestPoweroff:
    def test_poweroff(self, one: One, running_vm: int, action: str):
        vm_id = running_vm
        _id   = one.vm.action(action, vm_id)
        assert _id == vm_id

        wait_until(
            lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF,
            timeout_message=f"ВМ {vm_id} не выключилась",
            timeout=180
        )
    
    @pytest.mark.KERBEROS   
    def test_poweroff_KERBEROS(self, running_vm: int, action: str):
        vm_id   = running_vm
        pw      = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
        one     = pw.get_client()
        _id     = one.vm.action(action, vm_id, pw.sessionDir)
        pw.run_one_vm_action()

        assert _id == vm_id

        wait_until(
            lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF,
            timeout_message=f"ВМ {vm_id} не выключилась",
            timeout=180
        )









# @pytest.mark.skip(reason="Тестовый класс не готов")
# class TestReboot:
#     action = "reboot"
#     def test_reboot(self):
#         pass

# @pytest.mark.skip(reason="Тестовый класс не готов")
# class TestRebootHard:
#     action = "reboot-hard"
#     def test_reboot_hard(self):
#         pass



# @pytest.mark.skip(reason="Тестовый класс не готов")
# class TestHold:
#     action = "hold"
#     def test_hold(self):
#         pass

# @pytest.mark.skip(reason="Тестовый класс не готов")
# class TestRelease:
#     action = "release"
#     def test_release(self):
#         pass

# @pytest.mark.skip(reason="Тестовый класс не готов")
# class TestStop:
#     action = "stop"
#     def test_stop(self):
#         pass

# @pytest.mark.skip(reason="Тестовый класс не готов")
# class TestSuspend:
#     action = "suspend"
#     def test_suspend(self):
#         pass

# @pytest.mark.skip(reason="Тестовый класс не готов")
# class TestResume:
#     action = "resume"
#     def test_resume(self):
#         pass

# @pytest.mark.skip(reason="Тестовый класс не готов")
# class TestResched:
#     action = "resched"
#     def test_resched(self):
#         pass

# @pytest.mark.skip(reason="Тестовый класс не готов")
# class TestUnresched:
#     action = "unresched"
#     def test_unresched(self):
#         pass

    
