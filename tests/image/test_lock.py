import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException, OneActionException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte
from config             import API_URI, BRESTADM


BRESTADM_AUTH       = get_user_auth(BRESTADM)
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image():
    image_template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    image    = Image(image_id)
    
    yield image

    try:
        image.unlock()
    except Exception as _:
        pass

    image.delete()
    

# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.lock(999999, lock_level=4)



def test_lock_image_use(prepare_image):
    one         = One(BRESTADM_SESSION)
    image       = prepare_image
    lock_level  = 1

    assert image.info().LOCK == None
    one.image.lock(image._id, lock_level)
    assert image.info().LOCK.LOCKED == lock_level


def test_lock_image_manage(prepare_image):
    one         = One(BRESTADM_SESSION)
    image       = prepare_image
    lock_level  = 2

    assert image.info().LOCK == None
    one.image.lock(image._id, lock_level)
    assert image.info().LOCK.LOCKED == lock_level


def test_lock_image_admin(prepare_image):
    one         = One(BRESTADM_SESSION)
    image       = prepare_image
    lock_level  = 3

    assert image.info().LOCK == None
    one.image.lock(image._id, lock_level)
    assert image.info().LOCK.LOCKED == lock_level


def test_full_lock_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image       = prepare_image
    lock_level  = 4

    assert image.info().LOCK == None
    one.image.lock(image._id, lock_level)
    assert image.info().LOCK.LOCKED == lock_level


def test_reset_lock_level_image(prepare_image):
    one   = One(BRESTADM_SESSION)
    image = prepare_image

    assert image.info().LOCK == None

    for lock_level in [1, 2, 3, 4]:
        one.image.lock(image._id, lock_level=lock_level, check_already_locked=False)
        assert image.info().LOCK.LOCKED == lock_level



def test_check_if_image_locked(prepare_image):
    one   = One(BRESTADM_SESSION)
    image = prepare_image

    image.lock(lock_level=4)
    assert image.info().LOCK.LOCKED == 4

    for lock_level in [1, 2, 3, 4]:
        with pytest.raises(OneActionException):
            one.image.lock(image._id, lock_level=lock_level, check_already_locked=True)
        assert image.info().LOCK.LOCKED == 4
    

