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
    host_id = one.host.allocate("api_test_host_delete")
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
        one.host.delete(999999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_delete_host(one: One, host: Host):
    assert host_exist(host._id)
    one.host.delete(host._id)
    assert not host_exist(host._id)


