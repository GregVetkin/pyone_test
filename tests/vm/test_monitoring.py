import pytest
import time
from pyone              import OneException
from api                import One
from one_cli.vm         import VirtualMachine, create_vm
from config             import ADMIN_NAME, ADMIN_PASSWORD

VM_MONITOR_INTERVAL = 30 # Param MONITOR_VM in /etc/one/monitord.conf

@pytest.fixture()
def vm():
    vm_id = create_vm("CPU=1\nMEMORY=1\nVCPU=1", await_vm_offline=True)
    vm    = VirtualMachine(vm_id)
    yield vm
    vm.terminate()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(OneException):
        one.vm.monitoring(99999)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_monitoring(one: One, vm: VirtualMachine):
    time.sleep(VM_MONITOR_INTERVAL * 2)
    monitoring_before = one.vm.monitoring(vm._id)
    assert monitoring_before.has__content()

    time.sleep(VM_MONITOR_INTERVAL * 2)
    monitoring_after  = one.vm.monitoring(vm._id)
    assert monitoring_after.has__content()

    assert len(monitoring_before.MONITORING) < len(monitoring_after.MONITORING)