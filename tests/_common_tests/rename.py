import pytest
from pyone      import OneNoExistsException, OneActionException
from config     import BAD_SYMBOLS
from utils      import get_unic_name




def rename_if_not_exist__test(api_method) -> None:
    with pytest.raises(OneNoExistsException):
        api_method.rename(999999, "GregVetkin")



def rename__test(api_method, one_object) -> None:
    new_name = get_unic_name()
    api_method.rename(one_object._id, new_name)
    assert new_name == one_object.info().NAME



def rename_collision__test(api_method, one_object_1, one_object_2) -> None:
    old_name = one_object_1.info().NAME
    with pytest.raises(OneActionException):
        api_method.rename(one_object_1._id, one_object_2.info().NAME)
    new_name = one_object_1.info().NAME
    assert old_name == new_name



def rename_empty_name__test(api_method, one_object):
    old_name = one_object.info().NAME
    with pytest.raises(OneActionException):
        api_method.rename(one_object._id, "")
    new_name = one_object.info().NAME
    assert old_name == new_name



def rename_unavailable_symbol__test(api_method, one_object, bad_symbol):
    old_name = one_object.info().NAME

    with pytest.raises(OneActionException):
        api_method.rename(one_object._id, f"Greg{bad_symbol}")

    with pytest.raises(OneActionException):
        api_method.rename(one_object._id, f"{bad_symbol}Vetkin")
    
    with pytest.raises(OneActionException):
        api_method.rename(one_object._id, f"Greg{bad_symbol}Vetkin")
    
    with pytest.raises(OneActionException):
        api_method.rename(one_object._id, f"{bad_symbol}")

    new_name = one_object.info().NAME
    assert new_name == old_name

