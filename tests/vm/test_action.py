import pytest
import random
import pyone
import time

from utils.commands     import run_command_via_ssh
from utils.connection   import brest_admin_ssh_conn, local_admin_ssh_conn
from config.base        import API_URI, BrestAdmin, BREST_VERSION
from config.opennebula  import VmStates, VmLcmStates, VmRecoverOperations, VmActions
from utils.kerberos     import PyoneWrap
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
    
    vm_name = f"api_test_{random.randint(0, 9999)}" # С длинным именем из get_unic_name(), cli_prepare.sh не отрабатывает отлов статуса ВМ
    command = f"cd {script_dir} && ./cli_prepare.sh create_vm mini {vm_name} nonpers"
    
    run_command_via_ssh(ssh_conn, command)
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



@pytest.fixture
def pending_vm(one: One):
    template = '<VM><CPU><![CDATA[0.1]]></CPU><MEMORY><![CDATA[1]]></MEMORY><SCHED_DS_REQUIREMENTS><![CDATA[ID="99999"]]></SCHED_DS_REQUIREMENTS></VM>'
    vm_id = one.vm.allocate(template, False)
    yield vm_id
    one.vm.recover(vm_id, VmRecoverOperations.DELETE)


@pytest.fixture
def hold_vm(one: One):
    template = 'CPU=0.1\nMEMORY=1'
    vm_id = one.vm.allocate(template, True)
    yield vm_id
    one.vm.recover(vm_id, VmRecoverOperations.DELETE)




# =================================================================================================
# TESTS
# =================================================================================================


# def test_vm_not_exist(one: One):
#     action = "terminate"
#     vm_id  = 99999

#     with pytest.raises(OneNoExistsException):
#         one.vm.action(action, vm_id)


# def test_action_not_exist(one: One, dummy_vm: int):
#     action = "spamspamspam"
#     vm_id  = dummy_vm

#     with pytest.raises(OneActionException):
#         one.vm.action(action, vm_id)


# @pytest.mark.parametrize('action', [VmActions.TERMINATE, VmActions.TERMINATE_HARD])
# class TestTerminate:
#     def test_terminate(self, one: One, poweroff_vm: int, action: str):
#         vm_id = poweroff_vm
#         _id   = one.vm.action(action, vm_id)
#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.DONE,
#             timeout_message=f"ВМ {vm_id} не была удалена"
#         )
        
#     @pytest.mark.KERBEROS
#     def test_terminate_KERBEROS(self, poweroff_vm: int, action: str):
#         vm_id   = poweroff_vm
#         pw      = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#         one     = pw.get_client()
#         _id     = one.vm.action(action, vm_id, pw.sessionDir)
#         pw.run_one_vm_action()

#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.DONE,
#             timeout_message=f"ВМ {vm_id} не была удалена"
#         )


# @pytest.mark.parametrize('action', [VmActions.UNDEPLOY, VmActions.UNDEPLOY_HARD])
# class TestUndeploy:
#     def test_undeploy(self, one: One, poweroff_vm: int, action: str):
#         vm_id = poweroff_vm
#         _id   = one.vm.action(action, vm_id)
#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.UNDEPLOYED,
#             timeout_message=f"ВМ {vm_id} не получила статус 'Неразвернута'"
#         )

#     @pytest.mark.KERBEROS    
#     def test_undeploy_KERBEROS(self, poweroff_vm: int, action: str):
#         vm_id   = poweroff_vm
#         pw      = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#         one     = pw.get_client()
#         _id     = one.vm.action(action, vm_id, pw.sessionDir)
#         pw.run_one_vm_action()

#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.UNDEPLOYED,
#             timeout_message=f"ВМ {vm_id} не получила статус 'Неразвернута'"
#         )


# @pytest.mark.parametrize('action', [VmActions.POWEROFF, VmActions.POWEROFF_HARD])
# class TestPoweroff:
#     def test_poweroff(self, one: One, running_vm: int, action: str):
#         vm_id = running_vm
#         _id   = one.vm.action(action, vm_id)
#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF,
#             timeout_message=f"ВМ {vm_id} не выключилась",
#             timeout=180
#         )
    
#     @pytest.mark.KERBEROS   
#     def test_poweroff_KERBEROS(self, running_vm: int, action: str):
#         vm_id   = running_vm
#         pw      = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#         one     = pw.get_client()
#         _id     = one.vm.action(action, vm_id, pw.sessionDir)
#         pw.run_one_vm_action()

#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF,
#             timeout_message=f"ВМ {vm_id} не выключилась",
#             timeout=180
#         )



@pytest.mark.parametrize('action', [VmActions.REBOOT, VmActions.REBOOT_HARD])
class TestReboot:

    def test_reboot(self):
        pass

    @pytest.mark.KERBEROS
    def test_reboot_KERBEROS(self):
        pass



# class TestHold:
#     action = VmActions.HOLD

#     def test_hold(self, one: One, pending_vm: int):
#         vm_id = pending_vm
#         _id   = one.vm.action(self.action, vm_id)
#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.HOLD,
#             timeout_message=f"ВМ {vm_id} не перешла в статус УДЕРЖАНИЕ",
#         )
    
#     @pytest.mark.KERBEROS   
#     def test_hold_KERBEROS(self, pending_vm: int):
#         vm_id   = pending_vm
#         pw      = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#         one     = pw.get_client()
#         _id     = one.vm.action(self.action, vm_id, pw.sessionDir)
#         pw.run_one_vm_action()

#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.HOLD,
#             timeout_message=f"ВМ {vm_id} не перешла в статус УДЕРЖАНИЕ",
#         )


# class TestRelease:
#     action = VmActions.RELEASE

#     def test_release(self, one: One, hold_vm: int):
#         vm_id = hold_vm
#         _id   = one.vm.action(self.action, vm_id)
#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.PENDING,
#             timeout_message=f"ВМ {vm_id} не перешла в статус Ожидание",
#         )
#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF,
#             timeout_message=f"ВМ {vm_id} не разместилась на узле",
#         )
        
    
#     @pytest.mark.KERBEROS   
#     def test_release_KERBEROS(self, hold_vm: int):
#         vm_id   = hold_vm
#         pw      = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#         one     = pw.get_client()
#         _id     = one.vm.action(self.action, vm_id, pw.sessionDir)
#         pw.run_one_vm_action()

#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.PENDING,
#             timeout_message=f"ВМ {vm_id} не перешла в статус Ожидание",
#         )
#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.POWEROFF,
#             timeout_message=f"ВМ {vm_id} не разместилась на узле",
#         )


# class TestStop:
#     action = VmActions.STOP

#     def test_stop(self, one: One, running_vm: int):
#         vm_id = running_vm
#         _id   = one.vm.action(self.action, vm_id)
#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.STOPPED,
#             timeout_message=f"ВМ {vm_id} не перешла в статус ОСТАНОВЛЕНО",
#         )

        
    
#     @pytest.mark.KERBEROS   
#     def test_stop_KERBEROS(self, running_vm: int):
#         vm_id   = running_vm
#         pw      = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#         one     = pw.get_client()
#         _id     = one.vm.action(self.action, vm_id, pw.sessionDir)
#         pw.run_one_vm_action()

#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.STOPPED,
#             timeout_message=f"ВМ {vm_id} не перешла в статус ОСТАНОВЛЕНО",
#         )


# class TestSuspend:
#     action = VmActions.SUSPEND

#     def test_suspend(self, one: One, running_vm: int):
#         vm_id = running_vm
#         _id   = one.vm.action(self.action, vm_id)
#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.SUSPENDED,
#             timeout_message=f"ВМ {vm_id} не перешла в статус ПРИОСТАНОВЛЕНА",
#         )

        
#     @pytest.mark.KERBEROS   
#     def test_suspend_KERBEROS(self, running_vm: int):
#         vm_id   = running_vm
#         pw      = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#         one     = pw.get_client()
#         _id     = one.vm.action(self.action, vm_id, pw.sessionDir)
#         pw.run_one_vm_action()

#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).STATE == VmStates.SUSPENDED,
#             timeout_message=f"ВМ {vm_id} не перешла в статус ПРИОСТАНОВЛЕНА",
#         )


# class TestResume:
#     action = VmActions.RESUME

#     def test_resume(self, one: One, poweroff_vm: int):
#         vm_id = poweroff_vm
#         _id   = one.vm.action(self.action, vm_id)
#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).LCM_STATE == VmLcmStates.RUNNING,
#             timeout_message=f"ВМ {vm_id} не запутилась",
#         )

    
#     @pytest.mark.KERBEROS   
#     def test_resume_KERBEROS(self, poweroff_vm: int):
#         vm_id   = poweroff_vm
#         pw      = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#         one     = pw.get_client()
#         _id     = one.vm.action(self.action, vm_id, pw.sessionDir)
#         pw.run_one_vm_action()

#         assert _id == vm_id

#         wait_until(
#             lambda: one.vm.info(vm_id).LCM_STATE == VmLcmStates.RUNNING,
#             timeout_message=f"ВМ {vm_id} не запутилась",
#         )


# class TestResched:
#     action = VmActions.RESCHED

#     def test_resched(self, one: One, poweroff_vm: int):
#         vm_id       = poweroff_vm
#         host_before = one.vm.info(vm_id, True).HISTORY_RECORDS.HISTORY[-1].HID
#         _id         = one.vm.action(self.action, vm_id)

#         assert _id == vm_id
#         assert one.vm.info(vm_id, True).RESCHED == 1

#         wait_until(
#             lambda: one.vm.info(vm_id, True).LCM_STATE == VmLcmStates.PROLOG_MIGRATE_POWEROFF,
#             timeout_message=f"ВМ {vm_id} не была перенесена",
#         )
#         wait_until(lambda: one.vm.info(vm_id, True).STATE == VmStates.POWEROFF)

#         host_after = one.vm.info(vm_id, True).HISTORY_RECORDS.HISTORY[-1].HID
#         assert host_after != host_before



    
#     @pytest.mark.KERBEROS   
#     def test_resched_KERBEROS(self, poweroff_vm: int):
#         vm_id       = poweroff_vm
#         pw          = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#         one         = pw.get_client()
#         host_before = one.vm.info(vm_id, True).HISTORY_RECORDS.HISTORY[-1].HID
#         _id         = one.vm.action(self.action, vm_id, pw.sessionDir)
#         pw.run_one_vm_action()

#         assert _id == vm_id
#         assert one.vm.info(vm_id, True).RESCHED == 1

#         wait_until(
#             lambda: one.vm.info(vm_id, True).LCM_STATE == VmLcmStates.PROLOG_MIGRATE_POWEROFF,
#             timeout_message=f"ВМ {vm_id} не была перенесена",
#         )
#         wait_until(lambda: one.vm.info(vm_id, True).STATE == VmStates.POWEROFF)

#         host_after = one.vm.info(vm_id, True).HISTORY_RECORDS.HISTORY[-1].HID
#         assert host_after != host_before


# class TestUnresched:
#     action = VmActions.UNRESCHED

#     def test_unresched(self, one: One, poweroff_vm: int):
#         vm_id       = poweroff_vm
#         host_before = one.vm.info(vm_id, True).HISTORY_RECORDS.HISTORY[-1].HID

#         one.vm.action(VmActions.RESCHED, vm_id)
#         assert one.vm.info(vm_id, True).RESCHED == 1

#         _id = one.vm.action(self.action, vm_id)
#         assert _id == vm_id
#         assert one.vm.info(vm_id, True).RESCHED == 0

#         time.sleep(30)
#         host_after = one.vm.info(vm_id, True).HISTORY_RECORDS.HISTORY[-1].HID
#         assert host_after == host_before



    
#     @pytest.mark.KERBEROS   
#     def test_unresched_KERBEROS(self, poweroff_vm: int):
#         vm_id       = poweroff_vm
#         pw          = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
#         one         = pw.get_client()
#         host_before = one.vm.info(vm_id, True).HISTORY_RECORDS.HISTORY[-1].HID

#         one.vm.action(VmActions.RESCHED, vm_id)

#         # Вот здесь timeout 5 сек - resched может планировщиком быть обработан раньше, чем его отменим. 
#         # Нужно что-то придумать. Может передачу в функцию параметра таймаута? А по умолчанию 5 сек.
#         # Либо заморочиться и сделать выполнение функции в отдельном потоке/процессе, но стоит ли?
#         pw.run_one_vm_action()  
#         assert one.vm.info(vm_id, True).RESCHED == 1

#         _id = one.vm.action(self.action, vm_id, pw.sessionDir)
#         pw.run_one_vm_action()

#         assert _id == vm_id
#         assert one.vm.info(vm_id, True).RESCHED == 0

#         time.sleep(30)
#         host_after = one.vm.info(vm_id, True).HISTORY_RECORDS.HISTORY[-1].HID
#         assert host_after == host_before
