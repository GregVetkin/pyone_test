import pytest

from api                import One
from pyone              import OneNoExistsException, OneActionException
from utils              import get_user_auth, get_unic_name
from one_cli.image      import Image, create_image
from one_cli.datastore  import Datastore, create_datastore
from config             import BRESTADM, LOCK_LEVELS


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



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.lock(999999, lock_level=4)



@pytest.mark.parametrize("bad_lock_level", [5, 1024, -55])
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_bad_lock_level(one: One, image: Image, bad_lock_level):
    with pytest.raises(OneActionException):
        one.image.lock(image._id, bad_lock_level)



@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_lock_unlocked_image(one: One, image: Image, lock_level):
    assert image.info().LOCK == None
    one.image.lock(image._id, lock_level)
    assert image.info().LOCK.LOCKED == lock_level



@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("init_lock_lvl", LOCK_LEVELS)
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_lock_locked_image(one: One, image: Image, init_lock_lvl, lock_level, lock_check):
    image.lock(init_lock_lvl)
    assert image.info().LOCK.LOCKED == init_lock_lvl
    
    if lock_check:
        with pytest.raises(OneActionException):
            one.image.lock(image._id, lock_level=lock_level, check_already_locked=lock_check)
        assert image.info().LOCK.LOCKED == init_lock_lvl
    else:
        one.image.lock(image._id, lock_level=lock_level, check_already_locked=lock_check)
        assert image.info().LOCK.LOCKED == lock_level
