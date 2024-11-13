import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import Image, create_image
from one_cli.datastore  import Datastore, create_datastore
from one_cli.user       import User, create_user
from one_cli.group      import Group, create_group
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
    image.delete()
    

@pytest.fixture
def user():
    user_id = create_user("api_test_user")
    user    = User(user_id)
    yield user
    user.delete()


@pytest.fixture
def group():
    group_id = create_group("api_test_group")
    group    = Group(group_id)
    yield group
    group.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.chown(999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_user_not_exist(one: One, image: Image):
    image_old_info  = image.info()
    with pytest.raises(OneNoExistsException):
        one.image.chown(image._id, user_id=999999)
    image_new_info  = image.info()

    assert image_old_info.UID == image_new_info.UID



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_group_not_exist(one: One, image: Image):
    image_old_info  = image.info()
    with pytest.raises(OneNoExistsException):
        one.image.chown(image._id, group_id=999999)
    image_new_info  = image.info()

    assert image_old_info.GID == image_new_info.GID



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_user_and_group_change(one: One, image: Image, user: User, group: Group):
    one.image.chown(image._id, user._id, group._id)
    image_new_info = image.info()

    assert user._id  == image_new_info.UID
    assert group._id == image_new_info.GID



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_user_and_group_not_changed(one: One, image: Image):
    image_old_info = image.info()
    one.image.chown(image._id)
    image_new_info = image.info()
    
    assert image_old_info.UID == image_new_info.UID
    assert image_old_info.GID == image_new_info.GID



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_user_change(one: One, image: Image, user: User):
    image_old_info = image.info()
    one.image.chown(image._id, user_id=user._id)
    image_new_info = image.info()

    assert image_new_info.UID == user._id
    assert image_new_info.GID == image_old_info.GID



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_group_change(one: One, image: Image, group: Group):
    image_old_info = image.info()
    one.image.chown(image._id, group_id=group._id)
    image_new_info = image.info()

    assert image_new_info.UID == image_old_info.UID
    assert image_new_info.GID == group._id
