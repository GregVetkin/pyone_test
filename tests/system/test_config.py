from api    import One
from pyone  import OneServer
from utils  import get_brestadm_token


URI = "http://localhost:2633/RPC2"


def test_get_config_by_brestadm():
    one     = One(OneServer(URI, get_brestadm_token()))
    config  = one.system.config()
    assert config.has__content() == True
