import pytest
import time
from api                import One
from pyone              import OneActionException, OneNoExistsException
from utils              import get_user_auth
from one_cli.datastore  import Datastore, create_ds_by_tempalte, datastore_exist
from one_cli.image      import Image, create_image_by_tempalte, image_exist
from config             import BRESTADM


BRESTADM_AUTH    = get_user_auth(BRESTADM)


@pytest.fixture
def empty_datastore():
    datastore_template = """
        NAME   = api_test_system_ds
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore

    if datastore_exist(datastore._id):
        datastore.delete()


@pytest.fixture
def not_empty_datastore():
    datastore_template = """
        NAME   = api_test_system_ds
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)

    image_template = """
        NAME = api_test_datablock
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image_by_tempalte(datastore._id, image_template, True)
    image    = Image(image_id)

    yield datastore

    if not datastore_exist(datastore._id):
        return
    image.delete()
    while image_exist(image._id):
        time.sleep(2)
    datastore.delete()




# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.datastore.delete(999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_delete_empty_datastore(one: One, empty_datastore: Datastore):
    one.datastore.delete(empty_datastore._id)
    assert not datastore_exist(empty_datastore._id)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_delete_not_empty_datastore(one: One, not_empty_datastore: Datastore):
    with pytest.raises(OneActionException):
        one.datastore.delete(not_empty_datastore._id)
    assert datastore_exist(not_empty_datastore._id)