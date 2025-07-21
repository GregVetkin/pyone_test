import pytest

from api                            import One
from utils.other                    import wait_until
from config.opennebula              import ImageStates, VmStates
from config.tests                   import LOCK_LEVELS

from tests._common_methods.delete   import delete__test
from tests._common_methods.delete   import delete_if_not_exist__test
from tests._common_methods.delete   import cant_be_deleted__test



@pytest.fixture
def used_image(one: One, dummy_vm: int, dummy_image: int):
    vm_id    = dummy_vm
    image_id = dummy_image

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    one.vm.attach(vm_id, f"DISK=[IMAGE_ID={image_id}]")
    wait_until(lambda: one.image.info(image_id, False).STATE == ImageStates.USED)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    yield image_id

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    one.vm.detach(vm_id, 0)
    wait_until(lambda: one.image.info(image_id, False).STATE == ImageStates.READY)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)




# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist(one: One):
    delete_if_not_exist__test(one.image)



def test_ready_image(one: One, dummy_image: int):
    image_id = dummy_image
    delete__test(one.image, image_id)



def test_used_image(one: One, used_image: int):
    image_id = used_image
    cant_be_deleted__test(one.image, image_id)



@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_locked_image(one: One, dummy_image: int, lock_level: int):
    image_id = dummy_image

    one.image.lock(image_id, lock_level, False)
    wait_until(lambda: one.image.info(image_id, False).LOCK.LOCKED == lock_level)

    if lock_level == 3:
        delete__test(one.image, image_id)
    else:
        cant_be_deleted__test(one.image, image_id)
        
        one.image.unlock(image_id)
        wait_until(lambda: one.image.info(image_id, False).LOCK is None)

    