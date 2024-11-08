import pytest
import random

from api                import One
from pyone              import OneNoExistsException, OneAuthorizationException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte
from one_cli.datastore  import Datastore, create_ds_by_tempalte
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture(scope="module")
def datastore():
    datastore_template = """
        NAME   = api_test_image_ds
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def image(datastore: Datastore):
    template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image_by_tempalte(datastore._id, template)
    image    = Image(image_id)
    yield image
    if image.info().LOCK is not None:
        image.unlock()
    image.delete()


# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.update(99999, template="", replace=True)

    with pytest.raises(OneNoExistsException):
        one.image.update(99999, template="", replace=False)



#@pytest.mark.skip(reason="Нужна консультация по поводу провала при lock-level 4 (All). И уровне 3")
@pytest.mark.parametrize("lock_level", [1, 2, 3, 4])
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_locked_image(one: Image, image: Image, lock_level):
    image.lock(lock_level)
    assert lock_level == image.info().LOCK.LOCKED
    new_attribute_name = "TEST_ATTR"
    with pytest.raises(OneAuthorizationException):
        one.image.update(image._id, template=f"{new_attribute_name} = TEST_DATA")
    assert new_attribute_name not in image.info().TEMPLATE



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_image__replace(one: Image, image: Image):
    start_attribute_name = "START_ATTRIBUTE"
    image.update(f"{start_attribute_name} = TEST", append=True)

    new_attibutes = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template = "".join(f"{attr} = {_}\n" for _, attr in enumerate(new_attibutes))
    
    one.image.update(image._id, attr_template, replace=True)
    image_new_template = image.info().TEMPLATE

    for new_attribute in image_new_template:
        assert new_attribute in image_new_template

    assert start_attribute_name not in image_new_template



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_image__merge(one: Image, image: Image):
    start_attribute_name      = "START_ATTRIBUTE"
    image.update(f"{start_attribute_name} = TEST", append=True)
    start_attribute_new_value = "new_attr_value"

    new_attibutes  = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template  = "".join(f"{attr} = {_}\n" for _, attr in enumerate(new_attibutes))
    attr_template += f"{start_attribute_name} = {start_attribute_new_value}\n"

    one.image.update(image._id, attr_template, replace=False)
    image_new_template = image.info().TEMPLATE

    for new_attribute in image_new_template:
        assert new_attribute in image_new_template

    assert image_new_template[start_attribute_name] == start_attribute_new_value
