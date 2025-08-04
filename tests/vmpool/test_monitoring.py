import pytest
import pyone
import random
import time

from api             import One



VM_MONITOR_INTERVAL = 30 # Param MONITOR_VM in /etc/one/monitord.conf



# =================================================================================================
# TESTS
# =================================================================================================



# =================================================================================================
# TESTS
# =================================================================================================

@pytest.mark.parametrize("filtration", [-4, -3, -2, -1, 0, 1, 9999])
@pytest.mark.parametrize("last_secs", [-1, 0, 9999])
def test_monitoring_filters(one: One, filtration: int, last_secs: int):
    one.vmpool.monitoring(filtration, last_secs)
    # TODO: Дописать тесты


def test_monitoring_changes(one: One, running_vm_mini: int):
    records_before = one.vmpool.monitoring(-2, -1).MONITORING
    time.sleep(VM_MONITOR_INTERVAL * 2.5)
    records_after  = one.vmpool.monitoring(-2, -1).MONITORING
    assert len(records_before) < len(records_after)
    