import pytest
from typing             import List
from api                import One
from utils              import get_user_auth, get_unic_name
from one_cli.template   import Template, create_template
from config             import BRESTADM


BRESTADM_AUTH = get_user_auth(BRESTADM)



@pytest.fixture(scope="module")
def vmtemplates():
    vmtemplate_list = []
    for _ in range(5):
        template = f"""
            NAME    = {get_unic_name()}
            CPU     = 0.1
            VCPU    = 1
            MEMORY  = 32
        """
        vmtemplate_id   = create_template(template)
        vmtemplate      = Template(vmtemplate_id)
        vmtemplate_list.append(vmtemplate)

    yield vmtemplate_list

    for template in vmtemplate_list:
        template.delete()




# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_show_all_templates(one: One, vmtemplates: List[Template]):
    ids      = [vmtemplate._id for vmtemplate in vmtemplates]
    pool     = one.templatepool.info().VMTEMPLATE
    pool_ids = [vmtemplate.ID for vmtemplate in pool]

    assert set(ids).issubset(pool_ids)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_filter_start_id(one: One, vmtemplates: List[Template]):
    ids      = [vmtemplate._id for vmtemplate in vmtemplates]
    ids.sort()
    pool     = one.templatepool.info(start_id=ids[1]).VMTEMPLATE
    pool_ids = [vmtemplate.ID for vmtemplate in pool]
 
    assert ids[0] not in pool_ids
    assert set(ids[1:]).issubset(pool_ids)



@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_filter_end_id(one: One, vmtemplates: List[Template]):
    ids      = [vmtemplate._id for vmtemplate in vmtemplates]
    ids.sort()
    pool     = one.templatepool.info(start_id=ids[0], end_id=ids[-2]).VMTEMPLATE
    pool_ids = [vmtemplate.ID for vmtemplate in pool]

    assert ids[-1] not in pool_ids
    assert set(ids[:-2]).issubset(pool_ids)
