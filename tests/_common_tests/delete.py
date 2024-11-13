import pytest
from one_cli._base_commands     import _exist
from pyone                      import OneNoExistsException, OneActionException





def delete_if_not_exist__test(api_method) -> None:
    with pytest.raises(OneNoExistsException):
        api_method.delete(999999)




def delete__test(api_method, one_object) -> None:
    assert _exist(one_object._function, one_object._id)
    api_method.delete(one_object._id)
    assert not _exist(one_object._function, one_object._id)



def delete_undeletable__test(api_method, one_object) -> None:
    assert _exist(one_object._function, one_object._id)
    with pytest.raises(OneActionException):
        api_method.delete(one_object._id)
    assert _exist(one_object._function, one_object._id)
