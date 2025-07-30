import random
import xmlrpc.client

from api  import One





def test_get_default_quotas(one: One):
    # pyone возвращает неверный объект, поэтому проверка через прямой xmlrpc запрос
    server      = xmlrpc.client.ServerProxy(one._uri)
    image_id    = random.randint(1, 1024)
    rvms        = random.randint(1, 1024)

    default_quota_template  = f'IMAGE = [ID="{image_id}", RVMS="{rvms}"]'
    expected_string_part    = f"<IMAGE><ID><![CDATA[{image_id}]]></ID><RVMS><![CDATA[{rvms}]]></RVMS>"
    
    one.groupquota.update(default_quota_template)
    
    response = server.one.groupquota.info(one._session)


    assert response[0], "Вызов метода one.groupquota.info завершился ошибкой"
    assert expected_string_part in response[1]




