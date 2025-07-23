import pytest
import random
import time
from typing                         import List
from pyone                          import OneNoExistsException
from api                            import One
from utils.other                    import wait_until, get_unic_name
from config.tests                   import LOCK_LEVELS

from tests._common_methods.delete   import delete__test
from tests._common_methods.delete   import delete_if_not_exist__test
from tests._common_methods.delete   import cant_be_deleted__test



@pytest.fixture(params=LOCK_LEVELS)
def locked_template(one: One, dummy_template: int, request):
    template_id = dummy_template
    lock_level  = request.param

    one.template.lock(template_id, lock_level, False)
    wait_until(lambda: one.template.info(template_id, False).LOCK is not None)

    yield template_id

    try:
        one.template.unlock(template_id)
        wait_until(lambda: one.template.info(template_id, False).LOCK is None)

    except OneNoExistsException:
        return


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

    # for image_id in image_ids:
    #     one.image.delete(image_id, True)
    
    # wait_until(lambda: not one.datastore.info(datastore_id, False).IMAGES.ID)



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
    
    #one.template.delete(tempalte_id, False)


# =================================================================================================
# TESTS
# =================================================================================================




def test_template_not_exist(one: One):
    delete_if_not_exist__test(one.template)



def test_delete_template(one: One, dummy_template: int):
    template_id = dummy_template
    delete__test(one.template, template_id)



def test_locked_template(one: One, locked_template: int):
    template_id = locked_template

    if one.template.info(template_id).LOCK.LOCKED == 3:
        delete__test(one.template, template_id)
    else:
        cant_be_deleted__test(one.template, template_id)





def test_template_and_images(one: One, vmtemplate_with_images: int):
    template_id        = vmtemplate_with_images
    template_image_ids = [int(disk["IMAGE_ID"]) for disk in one.template.info(template_id, False, False).TEMPLATE["DISK"]]


    _id = one.template.delete(template_id, True)
    assert _id == template_id
    time.sleep(5)
    
    tempalte_pool = [tempalte.ID for tempalte in one.templatepool.info().VMTEMPLATE]
    image_pool    = [image.ID for image in one.imagepool.info().IMAGE]
    
    assert template_id not in tempalte_pool
    assert not set(image_pool) & set(template_image_ids)


