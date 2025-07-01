import pytest
import xmlrpc.client
from random     import randint
from api        import One



# =================================================================================================
# TESTS
# =================================================================================================



def test_update_default_quotas(one: One):
    # pyone возвращает неверный объект, поэтому проверка через прямой xmlrpc запрос
    server      = xmlrpc.client.ServerProxy(one._uri)
    image_id    = randint(1, 1024)
    rvms        = randint(1, 1024)

    default_quota_template  = f'IMAGE = [ID="{image_id}", RVMS="{rvms}"]'
    expected_string_part    = f"<IMAGE><ID><![CDATA[{image_id}]]></ID><RVMS><![CDATA[{rvms}]]></RVMS>"
    
    default_quotas_before_update = server.one.groupquota.info(one._session)
    assert expected_string_part not in default_quotas_before_update[1]

    server.one.groupquota.update(one._session, default_quota_template)

    default_quotas_before_update = server.one.groupquota.info(one._session)
    assert expected_string_part in default_quotas_before_update[1]




