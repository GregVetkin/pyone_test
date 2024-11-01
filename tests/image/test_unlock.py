import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte
from config             import API_URI, BRESTADM


BRESTADM_AUTH       = get_user_auth(BRESTADM)
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image():
    image_template  = """
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
        one.image.unlock(99999)


def test_unlock_locked_image(prepare_image):
    one   = One(BRESTADM_SESSION)
    image = prepare_image

    for lock_level in [1, 2, 3, 4]:
        image.lock(lock_level)
        assert image.info().LOCK.LOCKED == lock_level
        one.image.unlock(image._id)
        assert image.info().LOCK == None



def test_unlock_unlocked_image(prepare_image):
    one   = One(BRESTADM_SESSION)
    image = prepare_image

    assert image.info().LOCK == None
    one.image.unlock(image._id)
    assert image.info().LOCK == None

