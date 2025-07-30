import pytest
import pyone
import random

from api                import One
from utils.other        import get_unic_name



@pytest.fixture
def image_datastore(one: One):
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = dummy
        DS_MAD = dummy
    """
    _id = one.datastore.allocate(template, -1)
    yield _id
    one.datastore.delete(_id)


@pytest.fixture
def system_datastore(one: One):
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = SYSTEM_DS
        TM_MAD = dummy
    """
    _id = one.datastore.allocate(template, -1)
    yield _id
    one.datastore.delete(_id)




# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist(one: One):
    image_id     = random.randint(9999, 999999)
    clone_name   = get_unic_name()
    datastore_id = -1

    with pytest.raises(pyone.OneNoExistsException):
        one.image.clone(image_id, clone_name, datastore_id)



def test_datastore_not_exist(one: One, dummy_image: int):
    image_id     = dummy_image
    clone_name   = get_unic_name()
    datastore_id = random.randint(9999, 999999)

    with pytest.raises(pyone.OneNoExistsException):
        one.image.clone(image_id, clone_name, datastore_id)



def test_name_is_taken(one: One, dummy_image: int):
    image_id     = dummy_image
    clone_name   = one.image.info(image_id, False).NAME
    datastore_id = -1

    with pytest.raises(pyone.OneException):
        one.image.clone(image_id, clone_name, datastore_id)
    


def test_different_datastore_type(one: One, dummy_image: int, system_datastore: int):
    image_id     = dummy_image
    clone_name   = get_unic_name()
    datastore_id = system_datastore

    with pytest.raises(pyone.OneActionException):
        one.image.clone(image_id, clone_name, datastore_id)



def test_same_datastore(one: One, dummy_image: int):
    image_id     = dummy_image
    clone_name   = get_unic_name()
    datastore_id = -1
    clone_id     = one.image.clone(image_id, clone_name, datastore_id)

    assert one.image.info(clone_id, False).NAME == clone_name
    assert one.image.info(clone_id, False).DATASTORE_ID == one.image.info(image_id, False).DATASTORE_ID
    
    one.image.delete(clone_id, True)




def test_another_datastore(one: One, dummy_image: int, image_datastore: int):
    image_id     = dummy_image
    clone_name   = get_unic_name()
    datastore_id = image_datastore
    clone_id     = one.image.clone(image_id, clone_name, datastore_id)

    assert one.image.info(clone_id, False).NAME == clone_name
    assert one.image.info(clone_id, False).DATASTORE_ID == datastore_id
    
    one.image.delete(clone_id, True)
