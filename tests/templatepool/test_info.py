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
    ids      = vmtemplates
    pool_ids = [vmtemplate.ID for vmtemplate in one.templatepool.info().VMTEMPLATE]

    assert set(ids).issubset(pool_ids)




def test_filter_start_id(one: One, vmtemplates: List[int]):
    ids      = vmtemplates
    ids.sort()
    pool     = one.templatepool.info(start_id=ids[1]).VMTEMPLATE
    pool_ids = [vmtemplate.ID for vmtemplate in pool]
 
    assert ids[0] not in pool_ids
    assert set(ids[1:]).issubset(pool_ids)



def test_filter_end_id(one: One, vmtemplates: List[int]):
    ids      = vmtemplates
    ids.sort()
    pool     = one.templatepool.info(start_id=ids[0], end_id=ids[-2]).VMTEMPLATE
    pool_ids = [vmtemplate.ID for vmtemplate in pool]

    assert ids[-1] not in pool_ids
    assert set(ids[:-2]).issubset(pool_ids)
