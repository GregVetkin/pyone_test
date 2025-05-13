import pytest
from pyone       import OneNoExistsException, OneActionException
from utils.other import get_unic_name




def not_exist__test(api_object) -> None:
    with pytest.raises(OneNoExistsException):
        api_object.rename(999999, "GregoryVetkin")


def rename__test(api_object, one_object_id) -> None:
    new_name = get_unic_name()
    result   = api_object.rename(one_object_id, new_name)

    assert result   == one_object_id
    assert new_name == api_object.info(one_object_id).NAME


def cant_be_renamed__test(api_object, one_object_id, name):
    old_name = api_object.info(one_object_id).NAME

    with pytest.raises(OneActionException):
        api_object.rename(one_object_id, name)

    new_name = api_object.info(one_object_id).NAME
    assert old_name == new_name


