import pytest
import pyone

from api                import One
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

    with pytest.raises(pyone.OneInternalException):
        one.template.allocate(template)
    



def test_only_name(one: One):
    name = get_unic_name()
    template = f"NAME={name}"

    template_id = one.template.allocate(template)

    assert one.template.info(template_id, False, False).NAME == name
    one.template.delete(template_id, False)





def test_allocate_by_xml(one: One):
    name = get_unic_name()
    template = f"<VMTEMPLATE><NAME>{name}</NAME></VMTEMPLATE>"

    template_id = one.template.allocate(template)

    assert one.template.info(template_id, False, False).NAME == name
    one.template.delete(template_id, False)

