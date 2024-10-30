import pytest

from api                import One
from pyone              import OneServer, OneNoExistsException, OneActionException
from utils              import get_brestadm_auth
from commands.image     import delete_image, create_image_by_tempalte, unlock_image, get_image_lock_status, lock_image


URI                 = "http://localhost:2633/RPC2"
BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image():
    image_template  = """
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
        one.image.lock(999999, lock_level=4)


def test_lock_image_use(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    assert get_image_lock_status(image_id) == "None"
    one.image.lock(image_id, lock_level=1)
    assert get_image_lock_status(image_id) == "Use"


def test_lock_image_manage(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    assert get_image_lock_status(image_id) == "None"
    one.image.lock(image_id, lock_level=2)
    assert get_image_lock_status(image_id) == "Manage"


def test_lock_image_admin(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    assert get_image_lock_status(image_id) == "None"
    one.image.lock(image_id, lock_level=3)
    assert get_image_lock_status(image_id) == "Admin"


def test_full_lock_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    assert get_image_lock_status(image_id) == "None"
    one.image.lock(image_id, lock_level=4)
    assert get_image_lock_status(image_id) == "All"


def test_new_lock_level_image(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    assert get_image_lock_status(image_id) == "None"
    one.image.lock(image_id, lock_level=1, check_already_locked=False)
    assert get_image_lock_status(image_id) == "Use"
    one.image.lock(image_id, lock_level=2, check_already_locked=False)
    assert get_image_lock_status(image_id) == "Manage"
    one.image.lock(image_id, lock_level=3, check_already_locked=False)
    assert get_image_lock_status(image_id) == "Admin"
    one.image.lock(image_id, lock_level=4, check_already_locked=False)
    assert get_image_lock_status(image_id) == "All"


def test_check_if_image_locked(prepare_image):
    one         = One(BRESTADM_SESSION)
    image_id    = prepare_image
    lock_image(image_id, lock_level=4)
    assert get_image_lock_status(image_id) == "All"

    with pytest.raises(OneActionException):
        one.image.lock(image_id, lock_level=1, check_already_locked=True)
    assert get_image_lock_status(image_id) == "All"

    with pytest.raises(OneActionException):
        one.image.lock(image_id, lock_level=2, check_already_locked=True)
    assert get_image_lock_status(image_id) == "All"

    with pytest.raises(OneActionException):
        one.image.lock(image_id, lock_level=3, check_already_locked=True)
    assert get_image_lock_status(image_id) == "All"

    with pytest.raises(OneActionException):
        one.image.lock(image_id, lock_level=4, check_already_locked=True)
    assert get_image_lock_status(image_id) == "All"

