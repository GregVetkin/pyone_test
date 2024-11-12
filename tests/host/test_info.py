import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth
from one_cli.host       import Host, create_host, host_exist
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def host(one: One):
    host_id = one.host.allocate("api_test_host_info")
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
        one.host.info(999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_host_info(one: One, host: Host):
    api_host_info  = one.host.info(host._id)
    cli_host_info  = host.info()
    
    assert cli_host_info.ID    == api_host_info.ID
    assert cli_host_info.NAME  == api_host_info.NAME
    assert cli_host_info.STATE == api_host_info.STATE
