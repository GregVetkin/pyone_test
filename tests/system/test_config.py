from api    import One
from pyone  import OneServer
from utils  import get_brestadm_auth


URI                 = "http://localhost:2633/RPC2"
BRESTADM_AUTH       = get_brestadm_auth()
BRESTADM_SESSION    = OneServer(URI, BRESTADM_AUTH)



def test_get_config_by_brestadm():
    one     = One(BRESTADM_SESSION)
    config  = one.system.config()
    assert config.has__content() == True
