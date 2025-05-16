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
    with pytest.raises(OneInternalException):
        one.template.allocate("CPU=1\nVCPU=1\nMEMORY=32")
    


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_only_name_is_enough(one: One):
    _id = one.template.allocate(f"NAME = {get_unic_name()}")
    assert template_exist(_id)
    Template(_id).delete()




@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_creation_by_xml(one: One):
    _id = one.template.allocate(f"<VMTEMPLATE><NAME>{get_unic_name()}</NAME></VMTEMPLATE>")
    assert template_exist(_id)
    Template(_id).delete()

