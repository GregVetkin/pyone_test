import pytest

from api                import One
from utils              import get_user_auth, get_unic_name
from one_cli.image      import Image, create_image
from one_cli.datastore  import Datastore, create_datastore
from config             import BRESTADM, LOCK_LEVELS

from tests._common_tests.lock import lock_if_not_exist__test
from tests._common_tests.lock import lock_unlocked__test
from tests._common_tests.lock import lock_locked__test



BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture(scope="module")
def datastore():
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def image(datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
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


@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One, lock_level):
    lock_if_not_exist__test(one.image, lock_level)



@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_lock_unlocked_image(one: One, image: Image, lock_level):
    lock_unlocked__test(one.image, image, lock_level)



@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("init_lock_lvl", LOCK_LEVELS)
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_lock_locked_image(one: One, image: Image, init_lock_lvl, lock_level, lock_check):
    image.lock(init_lock_lvl)
    lock_locked__test(one.image, image, lock_level, lock_check)

