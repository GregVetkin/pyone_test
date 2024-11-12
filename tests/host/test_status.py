import pytest

from api                import One
from pyone              import OneNoExistsException, OneInternalException
from utils              import get_user_auth
from one_cli.host       import Host, create_host, host_exist
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture()
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def host(one: One):
    host_id = one.host.allocate("api_test_host_status")
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
        one.host.status(99999, 0)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_wrong_status_code(one: One, host: Host):
    with pytest.raises(OneInternalException):
        one.host.status(host._id, 9999)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_host_disable(one: One, host: Host):
    #one.host.status(host._id, 1)
    one.host.disable(host._id)
    assert host.info().STATE == 4   # 4 - DISABLED



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_host_offline(one: One, host: Host):
    #one.host.status(host._id, 2)
    one.host.offline(host._id)
    assert host.info().STATE == 8   # 8 - OFFLINE
    


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_host_enable(one: One, host: Host):
    #one.host.status(host._id, 0)
    one.host.enable(host._id)
    assert host.info().STATE in (0, 2, 3)   # 0 - INIT, 2 - ONLINE, 3 - ERROR
