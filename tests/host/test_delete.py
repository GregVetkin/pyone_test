from config.opennebula              import VmStates
from utils.other                    import wait_until
from api                            import One
from tests._common_methods.delete   import delete__test
from tests._common_methods.delete   import delete_if_not_exist__test
from tests._common_methods.delete   import cant_be_deleted__test








def test_host_not_exist(one: One):
   delete_if_not_exist__test(one.host)
   


def test_delete_empty_host(one: One, dummy_host):
    delete__test(one.host, dummy_host)



def test_cant_delete_host_with_vm(one: One, dummy_vm):
    wait_until(
        lambda: one.vm.info(dummy_vm).STATE == VmStates.POWEROFF,
        timeout_message=f"Истекло время ожидания размещения ВМ (ID:{dummy_vm})")

    host_id = one.vm.info(dummy_vm).HISTORY_RECORDS.HISTORY[-1].HID
    cant_be_deleted__test(one.host, host_id)
