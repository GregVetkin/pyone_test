import pytest
import random

from api                import One
from pyone              import OneNoExistsException
from utils              import get_user_auth
from one_cli.datastore  import Datastore, create_ds_by_tempalte
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)



@pytest.fixture
def datastore():
    datastore_template = """
        NAME   = api_test_system_ds
        TYPE   = SYSTEM_DS
        TM_MAD = ssh
    """
    datastore_id = create_ds_by_tempalte(datastore_template)
    datastore    = Datastore(datastore_id)
    yield datastore
    datastore.delete()



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_datastore_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.datastore.update(99999, template="", replace=True)
    with pytest.raises(OneNoExistsException):
        one.datastore.update(99999, template="", replace=False)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_datastore__replace(one: One, datastore: Datastore):
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    datastore.update(start_template, append=True)

    new_attributes = [f"ATTR_{_}" for _ in range(1, 3)]
    new_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(new_attributes))

    one.datastore.update(datastore._id, new_template, replace=True)
    datastore_new_attributes = datastore.info().TEMPLATE

    for start_attribute in start_attributes:
        assert start_attribute not in datastore_new_attributes

    for new_attribute in new_attributes:
        assert new_attribute in datastore_new_attributes



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_update_datastore__merge(one: One, datastore: Datastore):
    start_attributes = [f"START_ATTR_{_}" for _ in range(3)]
    start_template   = "".join(f"{attr} = {_}\n" for _, attr in enumerate(start_attributes))
    datastore.update(start_template, append=True)

    attribute_name       = random.choice(start_attributes)
    new_attribute_value  = "new_value"
    updated_attribute    = f"{attribute_name} = {new_attribute_value}"

    new_attibutes   = [f"ATTR_{_}" for _ in range(1, 6)]
    attr_template   = "".join(f"{attribute} = {_}\n" for _, attribute in enumerate(new_attibutes))
    attr_template   += updated_attribute

    one.datastore.update(datastore._id, attr_template, replace=False)
    datastore_new_attributes = datastore.info().TEMPLATE

    for new_attribute in new_attibutes:
        assert new_attribute in datastore_new_attributes

    for start_attribute in start_attributes:
        assert start_attribute in datastore_new_attributes
    
    assert datastore_new_attributes[attribute_name] == new_attribute_value
