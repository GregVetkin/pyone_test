import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException, OneActionException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte
from config             import API_URI, BRESTADM


BRESTADM_AUTH       = get_user_auth(BRESTADM)
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)
IMAGE_LOCK_LEVELS   = [1, 2, 3, 4]



@pytest.fixture
def prepare_image():
    image_template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template,)
    image    = Image(image_id)
    
    yield image

    if image.info().LOCK is not None:
        image.unlock()

    image.delete()
    

# =================================================================================================
# TESTS
# =================================================================================================


def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.lock(999999, lock_level=4)



@pytest.mark.parametrize("bad_lock_level", [5, 1024, -55])
def test_bad_lock_level(prepare_image, bad_lock_level):
    one         = One(BRESTADM_SESSION)
    image       = prepare_image
    with pytest.raises(OneActionException):
        one.image.lock(image._id, bad_lock_level)



@pytest.mark.parametrize("lock_level", IMAGE_LOCK_LEVELS)
def test_lock_unlocked_image(prepare_image, lock_level):
    one         = One(BRESTADM_SESSION)
    image       = prepare_image
    assert image.info().LOCK == None
    one.image.lock(image._id, lock_level)
    assert image.info().LOCK.LOCKED == lock_level



@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("init_lock_lvl", IMAGE_LOCK_LEVELS)
@pytest.mark.parametrize("lock_level", IMAGE_LOCK_LEVELS)
def test_lock_locked_image(prepare_image, init_lock_lvl, lock_level, lock_check):
    one   = One(BRESTADM_SESSION)
    image = prepare_image
    image.lock(init_lock_lvl)

    assert image.info().LOCK.LOCKED == init_lock_lvl
    
    if lock_check:
        with pytest.raises(OneActionException):
            one.image.lock(image._id, lock_level=lock_level, check_already_locked=lock_check)
        assert image.info().LOCK.LOCKED == init_lock_lvl
    else:
        one.image.lock(image._id, lock_level=lock_level, check_already_locked=lock_check)
        assert image.info().LOCK.LOCKED == lock_level


