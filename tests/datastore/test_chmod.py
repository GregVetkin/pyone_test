import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth
from one_cli.datastore  import Datastore, create_ds_by_tempalte
from config             import BRESTADM



BRESTADM_AUTH = get_user_auth(BRESTADM)




@pytest.fixture
def datastore():
    datastore_template = """
        NAME   = api_test_system_ds
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)

    datastore.chmod("000")
    yield datastore
    datastore.delete()




def datastore_rights(datastore_id: int):
    rights = Datastore(datastore_id).info().PERMISSIONS

    return ((rights.OWNER.USE, rights.OWNER.MANAGE, rights.OWNER.ADMIN),
            (rights.GROUP.USE, rights.GROUP.MANAGE, rights.GROUP.ADMIN),
            (rights.OTHER.USE, rights.OTHER.MANAGE, rights.OTHER.ADMIN))
    


# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.image.chmod(999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_change_datastore_rights(one: One, datastore: Datastore):
    datastore_id = datastore._id

    
    one.datastore.chmod(datastore_id, user_use=1)
    assert datastore_rights(datastore_id) == (  (True, False, False), 
                                                (False, False, False), 
                                                (False, False, False))

    one.datastore.chmod(datastore_id, user_manage=1)
    assert datastore_rights(datastore_id) == (  (True, True, False), 
                                                (False, False, False), 
                                                (False, False, False))

    one.datastore.chmod(datastore_id, user_admin=1)
    assert datastore_rights(datastore_id) == (  (True, True, True), 
                                                (False, False, False), 
                                                (False, False, False))

    one.datastore.chmod(datastore_id, user_admin=0)
    assert datastore_rights(datastore_id) == (  (True, True, False), 
                                                (False, False, False), 
                                                (False, False, False))

    one.datastore.chmod(datastore_id, user_manage=0)
    assert datastore_rights(datastore_id) == (  (True, False, False), 
                                                (False, False, False), 
                                                (False, False, False))
    
    one.datastore.chmod(datastore_id, user_use=0)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (False, False, False), 
                                                (False, False, False))



    one.datastore.chmod(datastore_id, group_use=1)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (True, False, False), 
                                                (False, False, False))

    one.datastore.chmod(datastore_id, group_manage=1)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (True, True, False), 
                                                (False, False, False))

    one.datastore.chmod(datastore_id, group_admin=1)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (True, True, True), 
                                                (False, False, False))

    one.datastore.chmod(datastore_id, group_admin=0)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (True, True, False), 
                                                (False, False, False))

    one.datastore.chmod(datastore_id, group_manage=0)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (True, False, False), 
                                                (False, False, False))
    
    one.datastore.chmod(datastore_id, group_use=0)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (False, False, False), 
                                                (False, False, False))



    one.datastore.chmod(datastore_id, other_use=1)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (False, False, False), 
                                                (True, False, False))

    one.datastore.chmod(datastore_id, other_manage=1)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (False, False, False), 
                                                (True, True, False))

    one.datastore.chmod(datastore_id, other_admin=1)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (False, False, False), 
                                                (True, True, True))

    one.datastore.chmod(datastore_id, other_admin=0)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (False, False, False), 
                                                (True, True, False))

    one.datastore.chmod(datastore_id, other_manage=0)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (False, False, False), 
                                                (True, False, False))
    
    one.datastore.chmod(datastore_id, other_use=0)
    assert datastore_rights(datastore_id) == (  (False, False, False), 
                                                (False, False, False), 
                                                (False, False, False))
