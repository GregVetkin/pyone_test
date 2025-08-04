import pytest
import pyone
import time
import random


from api                    import One
from config.base            import API_URI, BrestAdmin
from config.opennebula      import VmRecoverOperations, VmLcmStates, VmStates
from utils.other            import wait_until, get_unic_name
from utils.kerberos         import PyoneWrap






# =================================================================================================
# TESTS
# =================================================================================================




def test_vm_not_exist(one: One):
    vm_id = random.randint(9999, 999999)
    recover_operation = VmRecoverOperations.SUCCESS

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.recover(vm_id, recover_operation)




class TestFailure:
    recover_operation = VmRecoverOperations.FAILURE

    def test_code_0_failure(self, one: One, running_vm_mini: int):
        vm_id = running_vm_mini

        _id = one.vm.recover(vm_id, self.recover_operation)
        time.sleep(15)
        assert "ERROR" not in one.vm.info(vm_id, False).USER_TEMPLATE
        assert _id == vm_id


    @pytest.mark.KERBEROS
    def test_code_0_failure_KERBEROS(self, running_vm_mini: int):
        pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
        one = pw.get_client()

        vm_id = running_vm_mini

        _id = one.vm.recover(vm_id, self.recover_operation, pw.sessionDir)
        pw.run_one_vm_action()
        time.sleep(15)
        assert "ERROR" not in one.vm.info(vm_id, False).USER_TEMPLATE
        assert _id == vm_id



class TestSuccess:
    recover_operation = VmRecoverOperations.SUCCESS

    def test_code_1_success(self, one: One, running_vm_mini: int):
        vm_id = running_vm_mini

        _id = one.vm.recover(vm_id, self.recover_operation)
        time.sleep(15)
        assert "ERROR" not in one.vm.info(vm_id, False).USER_TEMPLATE
        assert _id == vm_id

    @pytest.mark.KERBEROS
    def test_code_1_success_KERBEROS(self, running_vm_mini: int):
        pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
        one = pw.get_client()

        vm_id = running_vm_mini

        _id = one.vm.recover(vm_id, self.recover_operation, pw.sessionDir)
        pw.run_one_vm_action()
        time.sleep(15)
        assert "ERROR" not in one.vm.info(vm_id, False).USER_TEMPLATE
        assert _id == vm_id



class TestRetry:
    recover_operation = VmRecoverOperations.RETRY

    def test_code_2_retry(self, one: One, running_vm_mini: int):
        vm_id = running_vm_mini

        _id = one.vm.recover(vm_id, self.recover_operation)
        time.sleep(15)
        assert "ERROR" not in one.vm.info(vm_id, False).USER_TEMPLATE
        assert _id == vm_id

    @pytest.mark.KERBEROS
    def test_code_2_retry_KERBEROS(self, running_vm_mini: int):
        pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
        one = pw.get_client()

        vm_id = running_vm_mini

        _id = one.vm.recover(vm_id, self.recover_operation, pw.sessionDir)
        pw.run_one_vm_action()
        time.sleep(15)
        assert "ERROR" not in one.vm.info(vm_id, False).USER_TEMPLATE
        assert _id == vm_id



class TestDelete:
    recover_operation = VmRecoverOperations.DELETE

    def test_code_3_delete(self, one: One, poweroff_vm_mini: int):
        vm_id = poweroff_vm_mini

        _id = one.vm.recover(vm_id, self.recover_operation)
        wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.DONE)

        assert "ERROR" not in one.vm.info(vm_id, False).USER_TEMPLATE
        assert _id == vm_id


    @pytest.mark.KERBEROS
    def test_code_3_delete_KERBEROS(self, one: One, poweroff_vm_mini: int):
        pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
        one = pw.get_client()

        vm_id = poweroff_vm_mini

        _id = one.vm.recover(vm_id, self.recover_operation, pw.sessionDir)
        pw.run_one_vm_action()
        wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.DONE)

        assert "ERROR" not in one.vm.info(vm_id, False).USER_TEMPLATE
        assert _id == vm_id



class TestDeleteRecreate:
    recover_operation = VmRecoverOperations.DELETE_RECREATE

    def test_code_4_delete_recreate(self, one: One, running_vm_mini: int):
        vm_id = running_vm_mini

        _id = one.vm.recover(vm_id, self.recover_operation)
        wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.CLEANUP_RESUBMIT)
        wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.PENDING, timeout=120)
        wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF, timeout=120)

        vm_info_after = one.vm.info(vm_id, False)

        assert "ERROR" not in vm_info_after.USER_TEMPLATE
        assert _id == vm_id
    

    @pytest.mark.KERBEROS
    def test_code_4_delete_recreate_KERBEROS(self, running_vm_mini: int):
        pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
        one = pw.get_client()

        vm_id = running_vm_mini

        _id = one.vm.recover(vm_id, self.recover_operation, pw.sessionDir)
        pw.run_one_vm_action()
        wait_until(lambda: one.vm.info(vm_id, False).LCM_STATE == VmLcmStates.CLEANUP_RESUBMIT)
        wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.PENDING, timeout=120)
        wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF, timeout=120)

        vm_info_after = one.vm.info(vm_id, False)

        assert "ERROR" not in vm_info_after.USER_TEMPLATE
        assert _id == vm_id



class TestDeleteDB:
    recover_operation = VmRecoverOperations.DELETE_DB


    def test_code_5_delete_db(self, one: One, poweroff_vm_mini: int):
        vm_id = poweroff_vm_mini

        _id = one.vm.recover(vm_id, self.recover_operation)
        wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.DONE)

        assert "ERROR" not in one.vm.info(vm_id, False).USER_TEMPLATE
        assert _id == vm_id


    @pytest.mark.KERBEROS
    def test_code_5_delete_db_KERBEROS(self, poweroff_vm_mini: int):
        pw  = PyoneWrap(API_URI, BrestAdmin.USERNAME, BrestAdmin.PASSWORD)
        one = pw.get_client()

        vm_id = poweroff_vm_mini

        _id = one.vm.recover(vm_id, self.recover_operation, pw.sessionDir)
        pw.run_one_vm_action()
        wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.DONE)

        assert "ERROR" not in one.vm.info(vm_id, False).USER_TEMPLATE
        assert _id == vm_id
