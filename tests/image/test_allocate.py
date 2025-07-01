import pytest
from utils.other        import get_unic_name
from api                import One
from pyone              import OneActionException, OneNoExistsException, OneException



@pytest.fixture
def system_datastore(one: One):
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = one.datastore.allocate(template, -1)

    yield datastore_id

    one.datastore.delete(datastore_id)


@pytest.fixture
def file_datastore(one: One):
    template = f"""
        NAME   = {get_unic_name()}
        TYPE   = FILE_DS
        TM_MAD = ssh
        DS_MAD = fs
    """
    datastore_id = one.datastore.allocate(template, -1)

    yield datastore_id

    one.datastore.delete(datastore_id)


# =================================================================================================
# TESTS
# =================================================================================================



def test_datastore_not_exist(one: One):
    datastore_id    = 999999
    check_capacity  = True
    template        = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    with pytest.raises(OneNoExistsException):
        one.image.allocate(template, datastore_id, check_capacity)



@pytest.mark.parametrize("check_capacity", [
    False,
    pytest.param(True, marks=pytest.mark.xfail(raises=OneActionException)),
])
def test_capaticy_check(one: One, dummy_datastore: int, check_capacity):
    datastore_id    = dummy_datastore
    template        = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1024000
    """
    image_id = one.image.allocate(template, datastore_id, check_capacity)

    assert one.image.info(image_id)

    one.image.delete(image_id, True)


@pytest.mark.parametrize("datastore_fixture_name", [
    "system_datastore",
    "file_datastore"
])
def test_wrong_datastore(one: One, datastore_fixture_name: str, request):
    datastore_id    = request.getfixturevalue(datastore_fixture_name)
    check_capacity  = False
    template        = f"""
        NAME = {get_unic_name()}
        TYPE = DATABLOCK
        SIZE = 1
    """
    with pytest.raises(OneException):
        one.image.allocate(template, datastore_id, check_capacity)



