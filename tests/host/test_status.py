import pytest

from api        import One
from config.config     import HostStates
from pyone      import OneNoExistsException, OneInternalException




# =================================================================================================
# TESTS
# =================================================================================================



def test_host_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.host.status(99999, 0)


def test_wrong_status_code(one: One, dummy_host):
    with pytest.raises(OneInternalException):
        one.host.status(dummy_host, 9999)


def test_host_disable(one: One, dummy_host):
    host_id = dummy_host
    result  = one.host._disable(host_id)
    assert result == host_id
    assert one.host.info(host_id).STATE == HostStates.DISABLED



def test_host_offline(one: One, dummy_host):
    host_id = dummy_host
    result  = one.host._offline(host_id)
    assert result == host_id
    assert one.host.info(host_id).STATE == HostStates.OFFLINE
    


def test_host_enable(one: One, dummy_host):
    host_id = dummy_host
    one.host._disable(host_id)
    result  = one.host._enable(host_id)
    assert result == host_id
    assert one.host.info(host_id).STATE not in (HostStates.DISABLED, HostStates.OFFLINE)
