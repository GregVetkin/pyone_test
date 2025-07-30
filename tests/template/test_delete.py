import pytest
import random
import pyone
import time

from typing                         import List
from api                            import One
from utils.other                    import wait_until, get_unic_name
from config.tests                   import LOCK_LEVELS
from tests._common_methods.delete   import delete__test, not_exist__test




@pytest.fixture(params=LOCK_LEVELS)
def locked_template(one: One, dummy_template: int, request):
    template_id = dummy_template
    lock_level  = request.param

    one.template.lock(template_id, lock_level, False)
    wait_until(lambda: one.template.info(template_id, False, False).LOCK is not None)

    yield template_id

    try:
        one.template.unlock(template_id)
        wait_until(lambda: one.template.info(template_id, False, False).LOCK is None)

    except pyone.OneNoExistsException:
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
        image_id = one.image.allocate(template, datastore_id, False)
        image_ids.append(image_id)
    
    yield image_ids

    if set(image_ids) & set([image.ID for image in one.imagepool.info(-2, -1, -1).IMAGE]):

        for image_id in image_ids:
            one.image.delete(image_id, True)
        wait_until(lambda: not one.datastore.info(datastore_id, False).IMAGES.ID)



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
    not_exist__test(one.template)



def test_delete_template(one: One, dummy_template: int):
    template_id = dummy_template
    delete__test(one.template, template_id)



def test_locked_template(one: One, locked_template: int):
    template_id = locked_template

    if one.template.info(template_id).LOCK.LOCKED == 3:
        delete__test(one.template, template_id)
    else:
        with pytest.raises(pyone.OneException):
            delete__test(one.template, template_id)




@pytest.mark.parametrize("delete_images", [True, False])
def test_template_and_images(one: One, vmtemplate_with_images: int, delete_images: bool):
    template_id        = vmtemplate_with_images
    template_image_ids = [int(disk["IMAGE_ID"]) for disk in one.template.info(template_id, False, False).TEMPLATE["DISK"]]


    _id = one.template.delete(template_id, delete_images)
    assert _id == template_id
    time.sleep(5)
    
    tempalte_pool = [tempalte.ID for tempalte in one.templatepool.info(-2, -1, -1).VMTEMPLATE]
    image_pool    = [image.ID for image in one.imagepool.info(-2, -1, -1).IMAGE]
    
    assert template_id not in tempalte_pool

    if delete_images:
        assert not set(image_pool) & set(template_image_ids)
    else:
        assert set(image_pool) & set(template_image_ids)

