import pytest
import pyone
from api                import One
from config.opennebula  import HostStates
from utils.other        import wait_until


@pytest.fixture
def offline_host(one: One, dummy_host):
    host_id = one.host.status(dummy_host, 2)
    yield host_id


@pytest.fixture
def disabled_host(one: One, dummy_host):
    host_id = one.host.status(dummy_host, 1)
    yield host_id



def test_host_not_exist(one: One):
    with pytest.raises(pyone.OneNoExistsException):
        one.host.status(99999, 0)


def test_wrong_status_code(one: One, dummy_host):
    with pytest.raises(pyone.OneInternalException):
        one.host.status(dummy_host, 9999)


def test_set_disable(one: One, dummy_host):
    host_id = dummy_host
    result  = one.host.status(host_id, 1)   # 1 - set Disable
    assert result == host_id
    assert one.host.info(host_id).STATE == HostStates.DISABLED



def test_set_offline(one: One, dummy_host):
    host_id = dummy_host
    result  = one.host.status(host_id, 2)   # 2 - set Offline
    assert result == host_id
    assert one.host.info(host_id).STATE == HostStates.OFFLINE
    


def test_enable_from_offline(one: One, offline_host):
    host_id = offline_host
    assert one.host.info(host_id).STATE == HostStates.OFFLINE
    result  = one.host.status(host_id, 0)   # 0 - set Enable

    wait_until(
        lambda: one.host.info(host_id).STATE != HostStates.OFFLINE,
        timeout_message="Хост не изменил статус с OFFLINE")
    
    assert result == host_id
    assert one.host.info(host_id).STATE not in (HostStates.DISABLED, HostStates.OFFLINE)



def test_enable_from_disable(one: One, disabled_host):
    host_id = disabled_host
    assert one.host.info(host_id).STATE == HostStates.DISABLED
    result  = one.host.status(host_id, 0)   # 0 - set Enable
    
    wait_until(
        lambda: one.host.info(host_id).STATE != HostStates.DISABLED,
        timeout_message="Хост не изменил статус с DISABLED")
    
    assert result == host_id
    assert one.host.info(host_id).STATE not in (HostStates.DISABLED, HostStates.OFFLINE)