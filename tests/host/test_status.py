import pytest

from api                import One
from pyone              import OneNoExistsException, OneInternalException
from utils              import get_unic_name
from one_cli.host       import Host, create_host, host_exist
from config             import ADMIN_NAME



# HOST_STATES = ['INIT', 'MONITORING_MONITORED', 'ENABLED',
#                 'ERROR','DISABLED', 'MONITORING_ERROR',
#                 'MONITORING_INIT','MONITORING_DISABLED', 'OFFLINE']

@pytest.fixture()
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def host(one: One):
    host_id = one.host.allocate(f"{get_unic_name()}")
    host    = Host(host_id)
    yield host
    if host_exist(host_id):
        host.delete()
    


# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.host.status(99999, 0)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_wrong_status_code(one: One, host: Host):
    with pytest.raises(OneInternalException):
        one.host.status(host._id, 9999)



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_disable(one: One, host: Host):
    #one.host.status(host._id, 1)
    one.host._disable(host._id)
    assert host.info().STATE == 4   # 4 - DISABLED



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_offline(one: One, host: Host):
    #one.host.status(host._id, 2)
    one.host._offline(host._id)
    assert host.info().STATE == 8   # 8 - OFFLINE
    


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_enable(one: One, host: Host):
    host.disable()
    #one.host.status(host._id, 0)
    one.host._enable(host._id)
    assert host.info().STATE not in (4, 8)
