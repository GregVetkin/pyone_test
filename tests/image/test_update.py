import pytest
import random

from api                import One
from pyone              import OneServer, OneNoExistsException, OneAuthorizationException
from utils              import get_user_auth
from one_cli.image      import Image, create_image_by_tempalte
from config             import API_URI, BRESTADM


BRESTADM_AUTH    = get_user_auth(BRESTADM)
BRESTADM_SESSION = OneServer(API_URI, BRESTADM_AUTH)





@pytest.fixture
def prepare_image_with_attr():
    image_template = """
        NAME = api_test_image
        TYPE = DATABLOCK
        SIZE = 10
        API_TEST_ATTR_1 = TEST_1
        API_TEST_ATTR_2 = TEST_2
    """
    image_id = create_image_by_tempalte(1, image_template, True)
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
        one.image.update(99999, template="", replace=True)

    with pytest.raises(OneNoExistsException):
        one.image.update(99999, template="", replace=False)



#@pytest.mark.skip(reason="Нужна консультация по поводу провала при lock-level 4 (All). И уровне 3")
@pytest.mark.parametrize("lock_level", [1, 2, 3, 4])
def test_update_locked_image(prepare_image_with_attr, lock_level):
    one   = One(BRESTADM_SESSION)
    image = prepare_image_with_attr

    image.lock(lock_level)
    image_lock_level = image.info().LOCK.LOCKED
    assert image_lock_level == lock_level

    with pytest.raises(OneAuthorizationException):
        attribute_name = "TEST_ATTR"
        one.image.update(image._id, template=f"{attribute_name} = TEST_DATA")

    image_attribute_names = image.info().TEMPLATE.keys()
    assert attribute_name not in image_attribute_names






@pytest.mark.skip(reason="Общий тест с параметризацией: test_update_image")
def test_update_image__replace(prepare_image_with_attr):
    one   = One(BRESTADM_SESSION)
    image = prepare_image_with_attr
    image_old_attribules = image.info().TEMPLATE

    new_attibutes = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template = "".join(f"{attr} = {_}\n" for _, attr in enumerate(new_attibutes))

    one.image.update(image._id, attr_template, replace=True)

    image_new_attribules = image.info().TEMPLATE

    for old_attr in image_old_attribules:
        assert old_attr not in image_new_attribules

    for new_attr in image_new_attribules:
        assert new_attr in image_new_attribules



@pytest.mark.skip(reason="Общий тест с параметризацией: test_update_image")
def test_update_image__merge(prepare_image_with_attr):
    one   = One(BRESTADM_SESSION)
    image = prepare_image_with_attr

    image_old_attribules = image.info().TEMPLATE

    attr_to_change = random.choice(list(image_old_attribules.keys()))
    attr_to_change_new_value = "new_attr_value"

    new_attibutes        = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template        = "".join(f"{attr} = {_}\n" for _, attr in enumerate(new_attibutes))
    attr_template       += f"{attr_to_change} = {attr_to_change_new_value}\n"

    one.image.update(image._id, attr_template, replace=False)

    image_new_attribules = image.info().TEMPLATE

    for new_attr in image_new_attribules:
        assert new_attr in image_new_attribules

    for old_attr in image_old_attribules:
        assert old_attr in image_new_attribules
    
    assert image_new_attribules[attr_to_change] == attr_to_change_new_value

    
@pytest.mark.parametrize("persistent", [True, False])
@pytest.mark.parametrize("disabled", [True, False])
@pytest.mark.parametrize("replace", [True, False])
def test_update_image(prepare_image_with_attr, replace, disabled, persistent):
    one   = One(BRESTADM_SESSION)
    image = prepare_image_with_attr

    if disabled:
        image.disable()

    if persistent:
        image.make_persistent()

    image_old_attribules = image.info().TEMPLATE

    new_attibutes = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template = "".join(f"{attr} = {_}\n" for _, attr in enumerate(new_attibutes))

    if not replace:
        attr_to_change = random.choice(list(image_old_attribules.keys()))
        attr_to_change_new_value = "new_attr_value"
        attr_template += f"{attr_to_change} = {attr_to_change_new_value}\n"

    one.image.update(image._id, attr_template, replace=replace)

    image_new_attribules = image.info().TEMPLATE

    for new_attr in image_new_attribules:
        assert new_attr in image_new_attribules

    if replace:
        for old_attr in image_old_attribules:
            assert old_attr not in image_new_attribules
    else:
        for old_attr in image_old_attribules:
            assert old_attr in image_new_attribules
        assert image_new_attribules[attr_to_change] == attr_to_change_new_value
