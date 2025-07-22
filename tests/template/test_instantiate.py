import pytest
import random

from typing             import List
from api                import One
from pyone              import OneNoExistsException

from utils.other        import wait_until
from utils.other        import get_unic_name

from config.opennebula  import VmStates
from config.opennebula  import ImageStates
from config.opennebula  import VmRecoverOperations




@pytest.fixture
def images(one: One, dummy_datastore: int):
    datastore_id = dummy_datastore
    image_ids    = []

    for _ in range(random.randint(2, 5)):
        template = f"""
            NAME = {get_unic_name()}
            TYPE = DATABLOCK
            SIZE = 1
        """
        image_id = one.image.allocate(template, datastore_id)
        image_ids.append(image_id)
    
    yield image_ids

    for image_id in image_ids:
        one.image.delete(image_id, True)
    
    deleted_ids_set = set(image_ids)

    wait_until(
        lambda: deleted_ids_set.isdisjoint(set(one.datastore.info(datastore_id, False).IMAGES.ID)),
        timeout_message="Some images were not removed when the test was completed."
        )



@pytest.fixture
def vmtemplate_with_images(one: One, images: List[int]):
    template = f"""
        NAME    = {get_unic_name()}
        CPU     = 1
        VCPU    = 2
        MEMORY  = 1024
    """
    for image_id in images:
        template += f"DISK=[IMAGE_ID={image_id}]\n"

    tempalte_id = one.template.allocate(template)

    yield tempalte_id
    
    one.template.delete(tempalte_id, False)


# =================================================================================================
# TESTS
# =================================================================================================




def test_template_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.template.instantiate(999999)




def test_vm_name(one: One, dummy_template: int):
    template_id     = dummy_template
    vm_name         = get_unic_name()
    hold_vm         = False
    extra_template  = "MEMORY=1\nCPU=1\nVCPU=1\n"
    pers_copy       = False

    vm_id = one.template.instantiate(template_id, vm_name, hold_vm, extra_template, pers_copy)
    wait_until(lambda: vm_id in [vm.ID for vm in one.vmpool.info().VM])
    
    assert one.vm.info(vm_id).NAME == vm_name

    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.DONE)




@pytest.mark.parametrize("hold_vm", [True, False])
def test_hold_vm(one: One, dummy_template: int, hold_vm: bool):
    template_id     = dummy_template
    vm_name         = get_unic_name()
    extra_template  = "MEMORY=1\nCPU=1\nVCPU=1\n"
    pers_copy       = False


    vm_id   = one.template.instantiate(template_id, vm_name, hold_vm, extra_template, pers_copy)
    wait_until(lambda: vm_id in [vm.ID for vm in one.vmpool.info().VM])
    vm_info = one.vm.info(vm_id)

    assert vm_info.NAME == vm_name

    if hold_vm:
        assert vm_info.STATE == VmStates.HOLD
    else:
        assert vm_info.STATE != VmStates.HOLD
    
    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.DONE)





def test_instantiane_with_extra_tempalte(one: One, dummy_template: int):
    template_id     = dummy_template
    vm_name         = get_unic_name()
    hold_vm         = True
    extra_template  = "MEMORY=1\nCPU=1\nVCPU=1\n"
    pers_copy       = False

    init_attr_name  = get_unic_name()
    init_attr_value = get_unic_name()
    init_template   = f"{init_attr_name} = {init_attr_value}"
    one.template.update(template_id, init_template, False)

    extra_attr_name  = get_unic_name()
    extra_attr_value = get_unic_name()
    extra_template   += f"{extra_attr_name} = {extra_attr_value}"

    vm_id = one.template.instantiate(template_id, vm_name, hold_vm, extra_template, pers_copy)
    wait_until(lambda: vm_id in [vm.ID for vm in one.vmpool.info().VM])

    vm_info = one.vm.info(vm_id)
    vm_user_template = vm_info.USER_TEMPLATE

    assert vm_info.NAME == vm_name
    assert vm_user_template[init_attr_name.upper()] == init_attr_value
    assert vm_user_template[extra_attr_name.upper()] == extra_attr_value
    
    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.DONE)






def test_private_persistent_copy(one: One, vmtemplate_with_images: int):
    template_id     = vmtemplate_with_images
    vm_name         = get_unic_name()
    hold_vm         = True
    pers_copy       = True
    extra_template  = "MEMORY=1\nCPU=1\nVCPU=1\n"

    init_attr_name  = get_unic_name()
    init_attr_value = get_unic_name()
    init_template   = f"{init_attr_name} = {init_attr_value}"
    one.template.update(template_id, init_template, False)

    template_images_ids = [int(disk["IMAGE_ID"]) for disk in one.template.info(template_id).TEMPLATE["DISK"]]


    vm_id = one.template.instantiate(template_id, vm_name, hold_vm, extra_template, pers_copy)
    wait_until(lambda: vm_id in [vm.ID for vm in one.vmpool.info().VM])

    vm_info          = one.vm.info(vm_id)
    vm_user_template = vm_info.USER_TEMPLATE
    vm_images_ids    = [int(disk["IMAGE_ID"]) for disk in one.vm.info(vm_id).TEMPLATE["DISK"]]

    assert vm_info.NAME == vm_name
    assert vm_user_template[init_attr_name.upper()] == init_attr_value

    assert len(template_images_ids) == len(vm_images_ids)
    assert max(template_images_ids) < min(vm_images_ids)
    assert not set(template_images_ids) & set(vm_images_ids)
  
    for image_id in vm_images_ids:
        image_info = one.image.info(image_id, False)
        assert image_info.PERSISTENT == 1
        assert image_info.STATE == ImageStates.USED_PERS
        

    one.vm.recover(vm_id, VmRecoverOperations.DELETE)
    wait_until(lambda: one.vm.info(vm_id).STATE == VmStates.DONE)

    for image_id in vm_images_ids:
        one.image.delete(image_id, True)
    
    deleted_ids_set = set(vm_images_ids)
    wait_until(
        lambda: deleted_ids_set.isdisjoint(set([image.ID for image in one.imagepool.info().IMAGE])),
        timeout_message="Some images were not removed when the test was completed."
        )
        
    
    
    