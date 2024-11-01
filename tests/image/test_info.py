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

    image.delete()
    

# =================================================================================================
# TESTS
# =================================================================================================


def test_image_not_exist():
    one = One(BRESTADM_SESSION)
    with pytest.raises(OneNoExistsException):
        one.image.info(999999)



def test_image_info(prepare_image):
    one   = One(BRESTADM_SESSION)
    image = prepare_image

    api_image_info  = one.image.info(image._id)
    cli_image_info  = image.info()
    
    assert cli_image_info.ID == api_image_info.ID
    assert cli_image_info.NAME == api_image_info.NAME
    assert cli_image_info.UNAME == api_image_info.UNAME
    assert cli_image_info.UID == api_image_info.UID
    assert cli_image_info.GNAME == api_image_info.GNAME
    assert cli_image_info.GID == api_image_info.GID
    assert cli_image_info.DATASTORE == api_image_info.DATASTORE
    assert cli_image_info.DATASTORE_ID == api_image_info.DATASTORE_ID
    assert cli_image_info.TYPE == api_image_info.TYPE
    assert cli_image_info.DISK_TYPE == api_image_info.DISK_TYPE
    assert cli_image_info.REGTIME == api_image_info.REGTIME
    assert cli_image_info.SOURCE == api_image_info.SOURCE
    assert cli_image_info.PATH == api_image_info.PATH
    assert cli_image_info.RUNNING_VMS == api_image_info.RUNNING_VMS
    assert cli_image_info.RUNNING_VMS == api_image_info.RUNNING_VMS
    assert cli_image_info.FORMAT == api_image_info.FORMAT
    assert cli_image_info.SIZE == api_image_info.SIZE
    assert cli_image_info.STATE == api_image_info.STATE
    assert cli_image_info.FS == api_image_info.FS

    persistence = {0: False, 1: True}
    assert cli_image_info.PERSISTENT == persistence[api_image_info.PERSISTENT]

    
