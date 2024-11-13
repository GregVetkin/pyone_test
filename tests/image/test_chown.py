import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth
from one_cli.image      import Image, create_image
from one_cli.datastore  import Datastore, create_datastore
from one_cli.user       import User, create_user
from one_cli.group      import Group, create_group
from config             import BRESTADM

from tests._common_tests.chown  import chown_object_not_exist__test
from tests._common_tests.chown  import chown_user_not_exist__test
from tests._common_tests.chown  import chown_group_not_exist__test
from tests._common_tests.chown  import chown_user_and_group_change__test
from tests._common_tests.chown  import chown_user_and_group_not_changed__test
from tests._common_tests.chown  import chown_user_change__test
from tests._common_tests.chown  import chown_group_change__test


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
    chown_object_not_exist__test(one.image)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_user_not_exist(one: One, image: Image):
    chown_user_not_exist__test(one.image, image)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_group_not_exist(one: One, image: Image):
    chown_group_not_exist__test(one.image, image)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_user_and_group_change(one: One, image: Image, user: User, group: Group):
    chown_user_and_group_change__test(one.image, image, user, group)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_user_and_group_not_changed(one: One, image: Image):
    chown_user_and_group_not_changed__test(one.image, image)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_user_change(one: One, image: Image, user: User):
    chown_user_change__test(one.image, image, user)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_group_change(one: One, image: Image, group: Group):
    chown_group_change__test(one.image, image, group)
