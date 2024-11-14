import pytest

from api                import One
from pyone              import OneActionException, OneNoExistsException, OneException
from utils              import get_user_auth, get_unic_name
from one_cli.image      import Image, create_image
from one_cli.datastore  import Datastore, create_datastore
from one_cli.user       import get_user_id_by_name
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture(scope="module")
def datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture(scope="module")
def datastore_2():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = IMAGE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture(scope="module")
def system_datastore():
    datastore_template = f"""
        NAME   = {get_unic_name()}
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_datastore(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()


@pytest.fixture
def image(datastore: Datastore):
    template = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    image_id = create_image(datastore._id, template)
    image    = Image(image_id)
    yield image
    image.delete()



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_image_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.clone(999999, get_unic_name())



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_not_exist(one: One, image: Image):
    with pytest.raises(OneNoExistsException):
        one.image.clone(image._id, get_unic_name(), 999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_name_is_taken(one: One, image: Image):
    brestadm_id = get_user_id_by_name("brestadm")
    if image.info().UID != brestadm_id:
        image.chown(brestadm_id)

    with pytest.raises(OneException):
        one.image.clone(image._id, image.info().NAME)
    


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_only_same_datastore_support(one: One, image: Image, system_datastore: Datastore):
    with pytest.raises(OneActionException):
        one.image.clone(image._id, "GregVetkin", system_datastore._id)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_clone_into_the_same_datastore(one: One, image: Image):
    clone_id = one.image.clone(image._id, get_unic_name())
    clone    = Image(clone_id)
    assert clone.info().DATASTORE_ID == image.info().DATASTORE_ID
    clone.delete()



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_clone_into_another_datastore(one: One, image: Image, datastore_2: Datastore):
    clone_id = one.image.clone(image._id, get_unic_name(), datastore_2._id)
    clone    = Image(clone_id)
    assert clone.info().DATASTORE_ID == datastore_2._id
    clone.delete()
