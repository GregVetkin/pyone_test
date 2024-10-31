import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException
from utils              import get_brestadm_auth
from commands.image     import delete_image, create_image_by_tempalte, unlock_image, lock_image, get_image_lock_status

from config             import API_URI


BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image():
    image_template  = f"""
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
    """
    image_id = create_image_by_tempalte(1, image_template, True)
    
    yield image_id

    unlock_image(image_id)
    delete_image(image_id)



# =================================================================================================
# TESTS
# =================================================================================================



def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.unlock(99999)


def test_unlock_locked_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image

    lock_image(image_id, lock_level=1)
    assert get_image_lock_status(image_id) == "Use"
    one.image.unlock(image_id)
    assert get_image_lock_status(image_id) == "None"

    lock_image(image_id, lock_level=2)
    assert get_image_lock_status(image_id) == "Manage"
    one.image.unlock(image_id)
    assert get_image_lock_status(image_id) == "None"

    lock_image(image_id, lock_level=3)
    assert get_image_lock_status(image_id) == "Admin"
    one.image.unlock(image_id)
    assert get_image_lock_status(image_id) == "None"

    lock_image(image_id, lock_level=4)
    assert get_image_lock_status(image_id) == "All"
    one.image.unlock(image_id)
    assert get_image_lock_status(image_id) == "None"


def test_unlock_unlocked_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image

    assert get_image_lock_status(image_id) == "None"
    one.image.unlock(image_id)
    assert get_image_lock_status(image_id) == "None"

