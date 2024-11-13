import pytest
from api                        import One
from utils                      import get_user_auth
from one_cli.image              import Image, create_image
from one_cli.datastore          import Datastore, create_datastore
from config                     import BRESTADM
from tests._common_tests.chmod  import chmod__test, chmod_if_not_exist__test


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
    image_template = """
        NAME = test_api_image
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(datastore._id, image_template)
    image    = Image(image_id)
    image.chmod("000")
    yield image
    image.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    chmod_if_not_exist__test(one.image)


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_change_image_rights(one: One, image: Datastore):
    chmod__test(one.image, image)

