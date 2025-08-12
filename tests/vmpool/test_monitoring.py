import pytest
import pyone
import random
import time

from api             import One



VM_MONITOR_INTERVAL = 30 # Param MONITOR_VM in /etc/one/monitord.conf


# =================================================================================================
# TESTS
# =================================================================================================



def test_monitoring_changes(one: One, running_vm_mini: int):
    records_before = one.vmpool.monitoring(-2, -1).MONITORING
    time.sleep(VM_MONITOR_INTERVAL * 3)
    records_after  = one.vmpool.monitoring(-2, -1).MONITORING
    assert len(records_before) < len(records_after)




def test_monitoring_vm_last_records(one: One):
    last_records = one.vmpool.monitoring(-2, 0).MONITORING
    vm_ids = [vm.ID for vm in last_records]
    assert len(last_records) == len(set(vm_ids))
