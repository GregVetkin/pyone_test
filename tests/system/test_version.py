from api    import One
from pyone  import OneServer
from utils  import get_brestadm_token



URI = "http://localhost:2633/RPC2"



def test_get_version_by_brestadm():
    one     = One(OneServer(URI, get_brestadm_token()))
    version = one.system.version()
    assert isinstance(version, str), "Полученный объект не является строкой"
