import pytest
import xmlrpc.client
import xml.etree.ElementTree as xmlTree

from api                    import One
from utils                  import get_unic_name, get_user_auth
from one_cli.group          import Group, create_group
from config                 import ADMIN_NAME, API_URI
from one_cli.group._common  import ImageQuotaInfo, NetworkQuotaInfo, DatastoreQuotaInfo, DefaultGroupQuotasInfo, parse_default_group_quotas







@pytest.fixture
def group():
    _id     = create_group(get_unic_name())
    group   = Group(_id)
    yield group
    group.delete()



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_get_default_quotas(one: One, group: Group):
    default_quota_template = ""

    image_quota = ImageQuotaInfo(
        ID= 999,
        RVMS= 999,
        RVMS_USED=0,
    )
    default_quota_template += f'IMAGE = [ID="{image_quota.ID}", RVMS="{image_quota.RVMS}"]'
    one.groupquota.update(default_quota_template)
    

    # pyone плохо работает с one.groupquota (возвращает обрубок xml)
    server      = xmlrpc.client.ServerProxy(API_URI)
    session     = get_user_auth(ADMIN_NAME)
    response    = server.one.groupquota.info(session)


    assert response[0], "Вызов метода one.groupquota.info() завершился ошибкой"
    default_quota_element   = xmlTree.fromstring(response[1])
    default_quota_info      = parse_default_group_quotas(default_quota_element)
    assert image_quota in default_quota_info.IMAGE_QUOTA

