import pytest

from api                import One
from pyone              import OneNoExistsException, OneActionException
from utils              import get_user_auth
from one_cli.host       import Host, create_host, host_exist
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def host(one: One):
    host_id = one.host.allocate("api_test_host_rename")
    host    = Host(host_id)
    yield host
    if host_exist(host_id):
        host.delete()
    


@pytest.fixture
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def host_2(one: One):
    host_id = one.host.allocate("api_test_host_rename_collision")
    host    = Host(host_id)
    yield host
    if host_exist(host_id):
        host.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_host_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.host.rename(99999, "GregoryVetkin")



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_rename_host(one: One, host: Host):
    new_name = "api_test_new_host_name"
    one.host.rename(host._id, new_name)
    assert host.info().NAME == new_name



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_host_name_collision(one: One, host: Host, host_2: Host):
    host_old_name = host.info().NAME
    with pytest.raises(OneActionException):
        one.host.rename(host._id, host_2.info().NAME)
    host_new_name = host.info().NAME
    assert host_old_name == host_new_name



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_empty_host_name(one: One, host: Host):
    host_old_name = host.info().NAME
    with pytest.raises(OneActionException):
        one.host.rename(host._id, "")
    host_new_name = host.info().NAME
    assert host_old_name == host_new_name



@pytest.mark.parametrize("symbol", ["$", "#", "&", "\"", "\'", ">", "<", "/", "\\", "|"])
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_unavailable_symbols_in_host_name(one: One, host: Host, symbol: str):
    host_old_name = host.info().NAME

    with pytest.raises(OneActionException):
        one.host.rename(host._id, f"test{symbol}")

    with pytest.raises(OneActionException):
        one.host.rename(host._id, f"{symbol}test")
    
    with pytest.raises(OneActionException):
        one.host.rename(host._id, f"te{symbol}st")
    
    with pytest.raises(OneActionException):
        one.host.rename(host._id, f"{symbol}")

    assert host.info().NAME == host_old_name

