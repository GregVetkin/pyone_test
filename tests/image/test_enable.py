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

    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)
    one.vm.detach(vm_id, 0)
    wait_until(lambda: one.image.info(image_id, False).STATE == ImageStates.READY)
    wait_until(lambda: one.vm.info(vm_id, False).STATE == VmStates.POWEROFF)








# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("enable", [True, False])
def test_image_not_exist(one: One, enable: bool):
    image_id = 999999
    with pytest.raises(OneNoExistsException):
        one.image.enable(image_id, enable)



@pytest.mark.parametrize("enable", [True, False])
def test_used_image(one: One, used_image: int, enable: bool):
    image_id = used_image

    assert one.image.info(image_id).STATE == ImageStates.USED

    with pytest.raises(OneInternalException):
        one.image.enable(image_id, enable)

    assert one.image.info(image_id).STATE == ImageStates.USED



@pytest.mark.parametrize(
    "start_status, expected_status",
    [
        (True, False),  # enabled  ->  disabled 
        (False, True),  # disabled ->  enabled
        (True, True),   # enabled  ->  enabled
        (False, False), # disabled ->  disabled
    ],
)
def test_image_status_toggle(one: One, dummy_image: int, start_status: bool, expected_status: bool):
    image_id         = dummy_image
    start_state_code = ImageStates.READY if start_status else ImageStates.DISABLED

    one.image.enable(image_id, start_status)
    wait_until(lambda: one.image.info(image_id).STATE == start_state_code)

    _id = one.image.enable(image_id, expected_status)
    assert _id == image_id

    if expected_status:
        assert one.image.info(image_id).STATE == ImageStates.READY
    else:
        assert one.image.info(image_id).STATE == ImageStates.DISABLED
