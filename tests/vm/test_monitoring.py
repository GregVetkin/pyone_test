import pytest
import pyone
import random
import time

from api             import One



VM_MONITOR_INTERVAL = 30 # Param MONITOR_VM in /etc/one/monitord.conf



# =================================================================================================
# TESTS
# =================================================================================================


def test_vm_not_exist(one: One):
    vm_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneNoExistsException):
        one.vm.monitoring(vm_id)




def test_monitoring(one: One, running_vm_mini: int):
    vm_id = running_vm_mini

    time.sleep(VM_MONITOR_INTERVAL * 2)
    monitoring_before = one.vm.monitoring(vm_id)
    assert monitoring_before.has__content()
    first_monitoring = monitoring_before.MONITORING[0]
    

    time.sleep(VM_MONITOR_INTERVAL * 2)
    monitoring_after = one.vm.monitoring(vm_id)
    assert monitoring_after.has__content()
    last_monitoring = monitoring_after.MONITORING[-1]

    assert len(monitoring_before.MONITORING) < len(monitoring_after.MONITORING)

    assert first_monitoring.ID == last_monitoring.ID
    assert first_monitoring.TIMESTAMP < last_monitoring.TIMESTAMP
