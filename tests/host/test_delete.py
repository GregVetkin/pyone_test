import time
from config.config                         import VmStates
from api                            import One
from tests._common_methods.delete   import delete__test
from tests._common_methods.delete   import delete_if_not_exist__test
from tests._common_methods.delete   import cant_be_deleted__test





# =================================================================================================
# TESTS
# =================================================================================================



def test_host_not_exist(one: One):
   delete_if_not_exist__test(one.host)
   


def test_delete_host(one: One, dummy_host):
    delete__test(one.host, dummy_host)



def test_cant_delete_host_with_vm(one: One, dummy_vm):
    while one.vm.info(dummy_vm).STATE != VmStates.POWEROFF: time.sleep(0.1)
    host_id = one.vm.info(dummy_vm).HISTORY_RECORDS.HISTORY[-1].HID
    cant_be_deleted__test(one.host, host_id)
