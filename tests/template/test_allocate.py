import pytest

from api                import One
from pyone              import OneInternalException
from utils              import get_user_auth, get_unic_name
from one_cli.template   import Template, create_template, template_exist
from config             import ADMIN_NAME, BAD_SYMBOLS






# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_tempalte_without_name(one: One):
    templ = "CPU=1 \n VCPU=1 \n MEMORY=32"
    with pytest.raises(OneInternalException):
        one.template.allocate(templ)
    



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_only_name_is_enough(one: One):
    _id = one.template.allocate(f"NAME = {get_unic_name()}")
    assert template_exist(_id)
    Template(_id).delete()



@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_with_unavailable_name(one: One, bad_symbol: str):
    
    with pytest.raises(OneInternalException):
        one.template.allocate(f"NAME = Greg{bad_symbol}")

    with pytest.raises(OneInternalException):
        one.template.allocate(f"NAME = {bad_symbol}Vetkin")
    
    with pytest.raises(OneInternalException):
        one.template.allocate(f"NAME = Greg{bad_symbol}Vetkin")
    
    with pytest.raises(OneInternalException):
        one.template.allocate(f"NAME = {bad_symbol}")




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_creation_by_xml(one: One):
    _id = one.template.allocate(f"<VMTEMPLATE><NAME>{get_unic_name()}</NAME></VMTEMPLATE>")
    assert template_exist(_id)
    Template(_id).delete()
