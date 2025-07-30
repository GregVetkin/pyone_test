import pytest
import pyone
from api                            import One
from tests._common_methods.delete   import delete__test, not_exist__test









def test_host_not_exist(one: One):
    not_exist__test(one.host)
   


def test_empty_host(one: One, dummy_host):
    delete__test(one.host, dummy_host)



def test_cant_delete_host_with_vm(one: One, poweroff_vm_mini):
    vm_id = poweroff_vm_mini
    host_id = one.vm.info(vm_id, False).HISTORY_RECORDS.HISTORY[-1].HID

    with pytest.raises(pyone.OneActionException):
        delete__test(one.host, host_id)