import pytest

from api                import One
from pyone              import OneAuthorizationException
from utils              import get_user_auth
from one_cli.image      import Image, create_image
from one_cli.datastore  import Datastore, create_datastore
from config             import BRESTADM


from tests._common_tests.update import update_and_merge__test
from tests._common_tests.update import update_and_replace__test
from tests._common_tests.update import update_if_not_exist__test



BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture(scope="module")
def datastore():
    datastore_template = """
        NAME   = api_test_image_ds
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
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
    image_id = create_image(datastore._id, template)
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
    update_if_not_exist__test(one.image)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_image__replace(one: Image, image: Image):
    update_and_replace__test(one.image, image)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_image__merge(one: Image, image: Image):
    update_and_merge__test(one.image, image)


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
