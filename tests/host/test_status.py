import pytest
import pyone
import random
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
    host_id = random.randint(9999, 999999)
    status = 0

    with pytest.raises(pyone.OneNoExistsException):
        one.host.status(host_id, status)


def test_wrong_status_code(one: One, dummy_host):
    host_id = dummy_host
    status = random.randint(9999, 999999)

    with pytest.raises(pyone.OneInternalException):
        one.host.status(host_id, status)


def test_set_disable(one: One, dummy_host):
    host_id = dummy_host
    status = 1  # 1 - set Disable

    _id = one.host.status(host_id, status)   
    assert _id == host_id
    assert one.host.info(host_id, False).STATE == HostStates.DISABLED



def test_set_offline(one: One, dummy_host):
    host_id = dummy_host
    status = 2  # 2 - set Offline

    _id = one.host.status(host_id, status)   
    assert _id == host_id
    assert one.host.info(host_id, False).STATE == HostStates.OFFLINE
    


def test_enable_from_offline(one: One, offline_host):
    host_id = offline_host
    status = 0  # 0 - set Enable

    assert one.host.info(host_id, False).STATE == HostStates.OFFLINE

    _id = one.host.status(host_id, status)   
    assert _id == host_id

    wait_until(
        lambda: one.host.info(host_id, False).STATE != HostStates.OFFLINE,
        timeout_message="Хост не изменил статус с OFFLINE")
    
    assert one.host.info(host_id, False).STATE not in (HostStates.DISABLED, HostStates.OFFLINE)



def test_enable_from_disable(one: One, disabled_host):
    host_id = disabled_host
    status = 0  # 0 - set Enable

    assert one.host.info(host_id, False).STATE == HostStates.DISABLED

    _id = one.host.status(host_id, status)
    assert _id == host_id

    wait_until(
        lambda: one.host.info(host_id, False).STATE != HostStates.DISABLED,
        timeout_message="Хост не изменил статус с DISABLED")
    
    assert one.host.info(host_id, False).STATE not in (HostStates.DISABLED, HostStates.OFFLINE)