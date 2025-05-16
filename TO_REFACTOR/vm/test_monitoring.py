import pytest
from pyone           import OneException, OneNoExistsException
from time            import sleep
from api             import One
from utils           import get_unic_name
from one_cli.vm      import VirtualMachine
from one_cli.image   import Image, create_image
from config          import ADMIN_NAME, VmStates


VM_MONITOR_INTERVAL = 30 # Param MONITOR_VM in /etc/one/monitord.conf



@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def image(one: One):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = one.image.allocate(template, 1)
    while one.image.info(image_id).STATE != 1: sleep(0.5)
    yield Image(image_id)
    while one.image.info(image_id).STATE != 1: sleep(0.5)
    one.image.delete(image_id)




@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def vm_with_disk(one: One, image: Image):
    vm_id = one.vm.allocate(f"NAME={get_unic_name()}\nCPU=0.1\nMEMORY=1\nDISK=[IMAGE_ID={image._id}]")
    while one.vm.info(vm_id).STATE != VmStates.POWEROFF: sleep(0.5)

    yield VirtualMachine(vm_id)

    one.vm.action("terminate-hard", vm_id)
    while one.vm.info(vm_id).STATE != VmStates.DONE: sleep(0.5)



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_vm_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.vm.monitoring(99999)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_monitoring(one: One, vm_with_disk: VirtualMachine):
    vm_id = vm_with_disk._id

    sleep(VM_MONITOR_INTERVAL * 2)
    monitoring_before = one.vm.monitoring(vm_id)
    assert monitoring_before.has__content()

    sleep(VM_MONITOR_INTERVAL * 2)
    monitoring_after  = one.vm.monitoring(vm_id)
    assert monitoring_after.has__content()

    assert len(monitoring_before.MONITORING) < len(monitoring_after.MONITORING)