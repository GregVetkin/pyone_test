import pytest
from one_cli._base_commands     import _exist
from pyone                      import OneNoExistsException





def test_delete_if_not_exist(api_method) -> None:
    with pytest.raises(OneNoExistsException):
        api_method.delete(999999)




def test_delete(api_method, one_object) -> None:
    assert _exist(one_object._function, one_object._id)
    api_method.delete(one_object._id)
    assert not _exist(one_object._function, one_object._id)





