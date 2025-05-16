import pytest
import pyone
from api                import One
from utils.other        import get_unic_name
from config.tests       import INVALID_CHARS



def test_create_group(one: One):
    group_name  = get_unic_name()
    group_id    = one.group.allocate(group_name)
    assert one.group.info(group_id).NAME == group_name
    one.group.delete(group_id)



def test_empty_name(one: One):
    with pytest.raises(pyone.OneInternalException):
        one.group.allocate("")



def test_name_is_taken(one: One):
    with pytest.raises(pyone.OneInternalException):
        one.group.allocate("brestadmins")



@pytest.mark.parametrize("char", INVALID_CHARS)
def test_invalid_char(one: One, char: str):
    with pytest.raises(pyone.OneInternalException):
        one.group.allocate(f"{char}")

    with pytest.raises(pyone.OneInternalException):
        one.group.allocate(f"{char}Vetkin")
    
    with pytest.raises(pyone.OneInternalException):
        one.group.allocate(f"Greg{char}")
    
    with pytest.raises(pyone.OneInternalException):
        one.group.allocate(f"Greg{char}Vetkin")

