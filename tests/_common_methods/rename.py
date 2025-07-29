import pytest
import random

from pyone       import OneNoExistsException, OneActionException
from utils.other import get_unic_name




def not_exist__test(api_object) -> None:
    one_object_id = random.randint(9999, 999999)
    new_name = "GregoryVetkin"

    with pytest.raises(OneNoExistsException):
        api_object.rename(one_object_id, new_name)


def rename__test(api_object, one_object_id: int, new_name: str) -> None:
    result = api_object.rename(one_object_id, new_name)

    assert result   == one_object_id
    assert new_name == api_object.info(one_object_id).NAME


def cant_be_renamed__test(api_object, one_object_id, name):
    old_name = api_object.info(one_object_id).NAME

    with pytest.raises(OneActionException):
        api_object.rename(one_object_id, name)

    new_name = api_object.info(one_object_id).NAME
    assert old_name == new_name


