import pytest

from api                import One
from pyone              import OneNoExistsException
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
    image.delete()


# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.unlock(99999)



@pytest.mark.parametrize("lock_level", [1, 2, 3, 4])
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_unlock_locked_image(one: One, image: Image, lock_level):
    image.lock(lock_level)
    assert image.info().LOCK.LOCKED == lock_level
    one.image.unlock(image._id)
    assert image.info().LOCK == None



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_unlock_unlocked_image(one: One, image: Image):
    assert image.info().LOCK == None
    one.image.unlock(image._id)
    assert image.info().LOCK == None
