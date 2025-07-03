import pytest

from api                import One
from pyone              import OneInternalException, OneNoExistsException
from utils.other        import wait_until
from config.opennebula  import ImageStates, VmStates



@pytest.fixture
def used_image(one: One, dummy_vm: int, dummy_image: int):
    vm_id    = dummy_vm
    image_id = dummy_image

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    one.vm.attach(vm_id, f"DISK=[IMAGE_ID={image_id}]")
    wait_until(lambda: one.image.info(image_id, False).STATE == ImageStates.USED)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    yield image_id

    one.vm.detach(vm_id, 0)
    wait_until(lambda: one.image.info(image_id, False).STATE == ImageStates.READY)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)




@pytest.fixture
def image_with_snapshot(one: One, dummy_vm: int, dummy_image: int):
    vm_id    = dummy_vm
    image_id = dummy_image

    one.image.persistent(image_id, True)
    wait_until(lambda: one.image.info(image_id, False).PERSISTENT == 1)

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    one.vm.attach(vm_id, f"DISK=[IMAGE_ID={image_id}]")
    wait_until(lambda: one.image.info(image_id, False).STATE == ImageStates.USED_PERS)

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    one.vm.disksnapshotcreate(vm_id, 0, "testsnap")
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)

    one.vm.detach(vm_id, 0)
    wait_until(lambda: one.image.info(image_id, False).STATE == ImageStates.READY)

    yield image_id

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    wait_until(lambda: one.image.info(image_id, False).STATE == ImageStates.READY)



# =================================================================================================
# TESTS
# =================================================================================================




def test_image_not_exist(one: One):
    image_id = 99999

    with pytest.raises(OneNoExistsException):
        one.image.persistent(image_id, True)

    with pytest.raises(OneNoExistsException):
        one.image.persistent(image_id, False)




def test_cant_change_persistence_for_used_image(one: One, used_image: int):
    image_id    = used_image
    persistence = one.image.info(image_id).PERSISTENT
    
    with pytest.raises(OneInternalException):
        one.image.persistent(image_id, True)
    assert one.image.info(image_id).PERSISTENT == persistence

    with pytest.raises(OneInternalException):
        one.image.persistent(image_id, False)
    assert one.image.info(image_id).PERSISTENT == persistence




def test_change_persistence(one: One, dummy_image: int):
    image_id = dummy_image

    _id = one.image.persistent(image_id, True)
    assert _id == image_id
    assert one.image.info(image_id, False).PERSISTENT == 1

    _id = one.image.persistent(image_id, False)
    assert _id == image_id
    assert one.image.info(image_id, False).PERSISTENT == 0




def test_cant_set_nonpers_for_image_with_snapshots(one: One, image_with_snapshot: int):
    image_id = image_with_snapshot

    with pytest.raises(OneInternalException):
        one.image.persistent(image_id, False)

    assert one.image.info(image_id).PERSISTENT == 1
