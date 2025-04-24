import pytest
import xmlrpc.client
import xml.etree.ElementTree as xmlTree
import random
import base64

from api                    import One
from utils                  import get_unic_name, get_user_auth
from one_cli.group          import Group, create_group
from config                 import ADMIN_NAME, API_URI, BREST_VERSION
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
def test_update_default_quotas(one: One, group: Group):
    default_quota_template = ""

    image_quota = ImageQuotaInfo(
        ID= random.randint(1, 1000),
        RVMS= random.randint(1, 1000),
        RVMS_USED=0,
    )
    default_quota_template += f'IMAGE = [ID="{image_quota.ID}", RVMS="{image_quota.RVMS}"]'


    old_group_default_quotas = group.info().DEFAULT_GROUP_QUOTAS
    assert image_quota not in old_group_default_quotas.IMAGE_QUOTA

    # pyone плохо работает с one.groupquota (возвращает обрубок xml), поэтому проверка через прямой xmlrpc запрос
    server    = xmlrpc.client.ServerProxy(API_URI)
    session   = get_user_auth(ADMIN_NAME)
    if BREST_VERSION == 4:
        session = base64.b64encode(session.encode()).decode()
    response  = server.one.groupquota.update(session, default_quota_template)

    assert response[0], "Вызов метода one.groupquota.update завершился ошибкой"
    default_quota_element  = xmlTree.fromstring(response[1])
    default_quota_info     = parse_default_group_quotas(default_quota_element)
    assert image_quota in default_quota_info.IMAGE_QUOTA


    new_group_default_quotas = group.info().DEFAULT_GROUP_QUOTAS
    assert image_quota in new_group_default_quotas.IMAGE_QUOTA

