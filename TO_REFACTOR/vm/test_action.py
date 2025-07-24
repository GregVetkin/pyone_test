import pytest
import random
import pyone

from config.base    import API_URI

from pyone          import OneNoExistsException
from pyone          import OneActionException
from api            import One







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






class TestTerminate:
    action = "terminate"
    def test_terminate_AIC(self, dummy_vm: int):
        
        assert self.action == "terminate"

class TestTerminateHard:
    action = "terminate-hard"
    def test_terminate_hard(self):
        pass



class TestUndeploy:
    action = "undeploy"
    def test_undeploy(self):
        pass

class TestUndeployHard:
    action = "undeploy-hard"
    def test_undeploy_hard(self):
        pass



class TestPoweroff:
    action = "poweroff"
    def test_poweroff(self):
        pass

class TestPoweroffHard:
    action = "poweroff-hard"
    def test_poweroff_hard(self):
        pass



class TestReboot:
    action = "reboot"
    def test_reboot(self):
        pass

class TestRebootHard:
    action = "reboot-hard"
    def test_reboot_hard(self):
        pass




class TestHold:
    action = "hold"
    def test_hold(self):
        pass


class TestRelease:
    action = "release"
    def test_release(self):
        pass


class TestStop:
    action = "stop"
    def test_stop(self):
        pass


class TestSuspend:
    action = "suspend"
    def test_suspend(self):
        pass


class TestResume:
    action = "resume"
    def test_resume(self):
        pass


class TestResched:
    action = "resched"
    def test_resched(self):
        pass


class TestUnresched:
    action = "unresched"
    def test_unresched(self):
        pass

    
