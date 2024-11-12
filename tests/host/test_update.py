import pytest
import random

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth
from one_cli.host       import Host, create_host, host_exist
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)



@pytest.fixture
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def host(one: One):
    host_id = one.host.allocate("api_test_host_update")
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
        one.host.update(99999, template="", replace=True)
    with pytest.raises(OneNoExistsException):
        one.host.update(99999, template="", replace=False)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_host__replace(one: One, host: Host):
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    host.update(start_template, append=True)

    new_attributes = [f"ATTR_{_}" for _ in range(1, 3)]
    new_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(new_attributes))

    one.host.update(host._id, new_template, replace=True)
    host_new_attributes = host.info().TEMPLATE

    for start_attribute in start_attributes:
        assert start_attribute not in host_new_attributes

    for new_attribute in new_attributes:
        assert new_attribute in host_new_attributes



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_host__merge(one: One, host: Host):
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    host.update(start_template, append=True)

    attribute_name       = random.choice(start_attributes)
    new_attribute_value  = "new_value"
    updated_attribute    = f"{attribute_name} = {new_attribute_value}"

    new_attibutes   = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template   = "".join(f"{attribute} = {_}\n" for _, attribute in enumerate(new_attibutes))
    attr_template   += updated_attribute

    one.host.update(host._id, attr_template, replace=False)
    host_new_attributes = host.info().TEMPLATE

    for new_attribute in new_attibutes:
        assert new_attribute in host_new_attributes

    for start_attribute in start_attributes:
        assert start_attribute in host_new_attributes
    
    assert host_new_attributes[attribute_name] == new_attribute_value
