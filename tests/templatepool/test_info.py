import pytest
from typing             import List
from api                import One
from utils.other        import get_unic_name




@pytest.fixture
def vmtemplates(one: One):
    vmtemplate_list = []
    for _ in range(5):
        template = f"""
            NAME    = {get_unic_name()}
            CPU     = 0.1
            VCPU    = 1
            MEMORY  = 32
        """
        vmtemplate_id = one.template.allocate(template)
        vmtemplate_list.append(vmtemplate_id)

    yield vmtemplate_list

    for vmtemplate_id in vmtemplate_list:
        one.template.delete(vmtemplate_id)




# =================================================================================================
# TESTS
# =================================================================================================




def test_show_all_templates(one: One, vmtemplates: List[int]):
    template_ids = vmtemplates

    filter_flag = -2
    start_id    = -1
    end_id      = -1

    pool_ids    = [vmtemplate.ID for vmtemplate in one.templatepool.info(filter_flag, start_id, end_id).VMTEMPLATE]

    assert set(template_ids).issubset(pool_ids)




def test_filter_start_id(one: One, vmtemplates: List[int]):
    template_ids = vmtemplates
    template_ids.sort()

    filter_flag = -2
    start_id    = template_ids[1]
    end_id      = -1

    pool        = one.templatepool.info(filter_flag, start_id, end_id).VMTEMPLATE
    pool_ids    = [vmtemplate.ID for vmtemplate in pool]
 
    assert template_ids[0] not in pool_ids
    assert set(template_ids[1:]).issubset(pool_ids)



def test_filter_end_id(one: One, vmtemplates: List[int]):
    template_ids = vmtemplates
    template_ids.sort()

    filter_flag = -2
    start_id    = template_ids[0]
    end_id      = template_ids[-2]

    pool        = one.templatepool.info(filter_flag, start_id, end_id).VMTEMPLATE
    pool_ids    = [vmtemplate.ID for vmtemplate in pool]

    assert template_ids[-1] not in pool_ids
    assert set(template_ids[:-2]).issubset(pool_ids)
