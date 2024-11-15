import pytest

from api                import One
from utils              import get_user_auth, get_unic_name
from one_cli.template   import Template, create_template
from one_cli.user       import User, create_user
from one_cli.group      import Group, create_group
from config             import BRESTADM

from tests._common_tests.chown  import chown_object_not_exist__test
from tests._common_tests.chown  import chown_user_not_exist__test
from tests._common_tests.chown  import chown_group_not_exist__test
from tests._common_tests.chown  import chown_user_and_group_change__test
from tests._common_tests.chown  import chown_user_and_group_not_changed__test
from tests._common_tests.chown  import chown_user_change__test
from tests._common_tests.chown  import chown_group_change__test


BRESTADM_AUTH = get_user_auth(BRESTADM)



@pytest.fixture(scope="module")
def user():
    user_id = create_user(get_unic_name())
    user    = User(user_id)
    yield user
    user.delete()

@pytest.fixture(scope="module")
def group():
    group_id = create_group(get_unic_name())
    group    = Group(group_id)
    yield group
    group.delete()




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
    if the_template.info().LOCK is not None:
        the_template.unlock()
    the_template.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_not_exist(one: One):
    chown_object_not_exist__test(one.template)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_user_not_exist(one: One, vmtemplate: Template):
    chown_user_not_exist__test(one.template, vmtemplate)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_group_not_exist(one: One, vmtemplate: Template):
    chown_group_not_exist__test(one.template, vmtemplate)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_user_and_group_change(one: One, vmtemplate: Template, user: User, group: Group):
    chown_user_and_group_change__test(one.template, vmtemplate, user, group)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_user_and_group_not_changed(one: One, vmtemplate: Template):
    chown_user_and_group_not_changed__test(one.template, vmtemplate)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_user_change(one: One, vmtemplate: Template, user: User):
    chown_user_change__test(one.template, vmtemplate, user)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_template_group_change(one: One, vmtemplate: Template, group: Group):
    chown_group_change__test(one.template, vmtemplate, group)
