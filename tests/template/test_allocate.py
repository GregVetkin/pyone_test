import pytest

from api                import One
from pyone              import OneInternalException
from utils.other        import get_unic_name





# =================================================================================================
# TESTS
# =================================================================================================




def test_name_is_mandatory(one: One):
    template = """
        CPU     = 1
        VCPU    = 1
        MEMORY  = 32
    """

    with pytest.raises(OneInternalException):
        one.template.allocate(template)
    



def test_only_name(one: One):
    name     = get_unic_name()
    template = f"NAME={name}"
    _id      = one.template.allocate(template)

    assert one.template.info(_id).NAME == name
    one.template.delete(_id, False)





def test_creation_by_xml(one: One):
    name     = get_unic_name()
    template = f"<VMTEMPLATE><NAME>{name}</NAME></VMTEMPLATE>"

    _id = one.template.allocate(template)
    assert one.template.info(_id).NAME == name
    one.template.delete(_id, False)

