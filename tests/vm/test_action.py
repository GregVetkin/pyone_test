import pytest
import random
import pyone


from utils.commands     import run_command_via_ssh
from utils.connection   import brest_admin_ssh_conn
from config.base        import API_URI
from config.base        import BrestAdmin
from config.opennebula  import VmStates, VmLcmStates
from utils.aic          import PyoneWrap
from utils.other        import wait_until
from pyone              import OneNoExistsException
from pyone              import OneActionException
from api                import One




@pytest.fixture
def poweroff_dummy_vm(one: One, dummy_vm: int):
    vm_id = dummy_vm
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF)
    yield vm_id
    

@pytest.fixture
def running_dummy_vm(one: One, poweroff_dummy_vm: int):
    vm_id = poweroff_dummy_vm
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

    def test_terminate(self, one: One, poweroff_dummy_vm: int, action: str):
        vm_id = poweroff_dummy_vm
        _id   = one.vm.action(action, vm_id)
        assert _id == vm_id

        wait_until(
            lambda: one.vm.info(vm_id).STATE == VmStates.DONE,
            timeout_message=f"ВМ {vm_id} не была удалена"
        )
        
    def test_terminate_KERBEROS(self, poweroff_dummy_vm: int, action: str):
        vm_id = poweroff_dummy_vm
        pw = PyoneWrap(
            ip="10.0.70.21", 
            auth_user=BrestAdmin.USERNAME,
            auth_pass=BrestAdmin.PASSWORD
        )
        one = pw.get_client()
        _id = one.vm.action(action, vm_id, pw.sessionDir)
        pw.run_one_vm_action()

        assert _id == vm_id

        wait_until(
            lambda: one.vm.info(vm_id).STATE == VmStates.DONE,
            timeout_message=f"ВМ {vm_id} не была удалена"
        )



@pytest.mark.parametrize('action', ["undeploy", "undeploy-hard"])
class TestUndeploy:

    def test_undeploy(self, one: One, poweroff_dummy_vm: int, action: str):
        vm_id = poweroff_dummy_vm
        _id   = one.vm.action(action, vm_id)
        assert _id == vm_id

        wait_until(
            lambda: one.vm.info(vm_id).STATE == VmStates.UNDEPLOYED,
            timeout_message=f"ВМ {vm_id} не получила статус 'Неразвернута'"
        )
        
    def test_undeploy_KERBEROS(self, poweroff_dummy_vm: int, action: str):
        vm_id = poweroff_dummy_vm
        pw = PyoneWrap(
            ip="10.0.70.21", 
            auth_user=BrestAdmin.USERNAME,
            auth_pass=BrestAdmin.PASSWORD
        )
        one = pw.get_client()
        _id = one.vm.action(action, vm_id, pw.sessionDir)
        pw.run_one_vm_action()

        assert _id == vm_id

        wait_until(
            lambda: one.vm.info(vm_id).STATE == VmStates.UNDEPLOYED,
            timeout_message=f"ВМ {vm_id} не получила статус 'Неразвернута'"
        )




@pytest.mark.parametrize('action', ["poweroff", "poweroff-hard"])
class TestPoweroff:

    def test_poweroff(self, one: One, running_dummy_vm: int, action: str):
        vm_id = running_dummy_vm
        _id   = one.vm.action(action, vm_id)
        assert _id == vm_id

        wait_until(
            lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF,
            timeout_message=f"ВМ {vm_id} не выключилась"
        )
        
    def test_poweroff_KERBEROS(self, running_dummy_vm: int, action: str):
        vm_id = running_dummy_vm
        pw = PyoneWrap(
            ip="10.0.70.21", 
            auth_user=BrestAdmin.USERNAME,
            auth_pass=BrestAdmin.PASSWORD
        )
        one = pw.get_client()
        _id = one.vm.action(action, vm_id, pw.sessionDir)
        pw.run_one_vm_action()

        assert _id == vm_id

        wait_until(
            lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF,
            timeout_message=f"ВМ {vm_id} не выключилась"
        )




@pytest.mark.skip(reason="Тестовый класс не готов")
class TestReboot:
    action = "reboot"
    def test_reboot(self):
        pass

@pytest.mark.skip(reason="Тестовый класс не готов")
class TestRebootHard:
    action = "reboot-hard"
    def test_reboot_hard(self):
        pass



@pytest.mark.skip(reason="Тестовый класс не готов")
class TestHold:
    action = "hold"
    def test_hold(self):
        pass

@pytest.mark.skip(reason="Тестовый класс не готов")
class TestRelease:
    action = "release"
    def test_release(self):
        pass

@pytest.mark.skip(reason="Тестовый класс не готов")
class TestStop:
    action = "stop"
    def test_stop(self):
        pass

@pytest.mark.skip(reason="Тестовый класс не готов")
class TestSuspend:
    action = "suspend"
    def test_suspend(self):
        pass

@pytest.mark.skip(reason="Тестовый класс не готов")
class TestResume:
    action = "resume"
    def test_resume(self):
        pass

@pytest.mark.skip(reason="Тестовый класс не готов")
class TestResched:
    action = "resched"
    def test_resched(self):
        pass

@pytest.mark.skip(reason="Тестовый класс не готов")
class TestUnresched:
    action = "unresched"
    def test_unresched(self):
        pass

    
