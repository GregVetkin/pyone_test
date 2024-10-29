import pytest

from api                import One
from pyone              import OneServer, OneActionException, OneNoExistsException, OneException
from utils              import get_brestadm_auth, run_command
from commands.images    import is_image_exist, delete_image, wait_image_rdy


URI                 = "http://localhost:2633/RPC2"
BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(URI, BRESTADM_AUTH)



ERROR_GETTING_IMAGE     = "Error getting image"
ERROR_GETTING_DATASTORE = "Error getting datastore"
ERROR_NAME_IS_TAKEN     = "NAME is already taken"
ERROR_CLONE_SUPPORT     = "Clone only supported for IMAGE_DS Datastores"


@pytest.fixture
def prepare_image_datablock():
    image_name  = "api_test_image"
    image_id    = int(run_command(f"sudo oneimage create -d 1 --name {image_name} --type DATABLOCK --size 10 " + " | awk '{print $2}'"))
    wait_image_rdy(image_id)
    
    yield (image_id, image_name)

    run_command(f"sudo oneimage delete {image_id}")


@pytest.fixture
def prepare_image_datastore():
    template_file_path  = "/tmp/test_template_file"
    datastore_name      = "api_test_image_ds"
    datastore_template  = f"""
        NAME = {datastore_name}
        TYPE = IMAGE_DS
        DS_MAD = fs
        TM_MAD = ssh
    """
    with open(template_file_path, "w") as template_file:
        template_file.write(datastore_template)

    datastore_id   = int(run_command(f"sudo onedatastore create {template_file_path} " + " | awk '{print $2}'"))
    
    yield datastore_id, datastore_name
    
    run_command(f"sudo onedatastore delete {datastore_id}")


def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException, match=ERROR_GETTING_IMAGE):
        one.image.clone(999999, "")


def test_datastore_not_exist(prepare_image_datablock):
    one         = One(BRESTADM_SESSION)
    image_id, _ = prepare_image_datablock
    with pytest.raises(OneNoExistsException, match=ERROR_GETTING_DATASTORE):
        one.image.clone(image_id, "GregVetkin", 999999)


def test_name_is_taken(prepare_image_datablock):
    one                  = One(BRESTADM_SESSION)
    image_id, image_name = prepare_image_datablock
    with pytest.raises(OneException, match=ERROR_NAME_IS_TAKEN):
        one.image.clone(image_id, image_name)


def test_only_image_datastore_support(prepare_image_datablock):
    one         = One(BRESTADM_SESSION)
    image_id, _ = prepare_image_datablock
    with pytest.raises(OneActionException, match=ERROR_CLONE_SUPPORT):
        one.image.clone(image_id, "GregVetkin", 2)


def test_clone_into_the_same_datastore(prepare_image_datablock):
    one         = One(BRESTADM_SESSION)
    image_id, _ = prepare_image_datablock
    clone_id    = one.image.clone(image_id, "api_test_image_clone")
    assert is_image_exist(clone_id) == True
    delete_image(clone_id)


def test_clone_into_another_datastore(prepare_image_datablock, prepare_image_datastore):
    one             = One(BRESTADM_SESSION)
    image_id, _     = prepare_image_datablock
    datastore_id, _ = prepare_image_datastore
    clone_id        = one.image.clone(image_id, "api_test_image_clone", datastore_id)
    assert is_image_exist(clone_id) == True
    delete_image(clone_id)
