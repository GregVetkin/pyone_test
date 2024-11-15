import pytest

from api                import One
from pyone              import OneNoExistsException
from utils              import get_unic_name
from one_cli.template   import Template, create_template, template_exist
from config             import ADMIN_NAME





@pytest.fixture
def vmtemplate():
    template = f"""
        NAME    = {get_unic_name()}
        CPU     = 1
        VCPU    = 2
        MEMORY  = 1024
    """
    _id = create_template(template)
    the_template = Template(_id)
    yield the_template
    the_template.delete()
    



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_template_not_exist(one: One):
    with pytest.raises(OneNoExistsException):
        one.template.instantiate(999999)



