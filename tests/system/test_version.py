from api        import One
from pyone      import OneServer
from utils      import get_user_auth
from config     import API_URI, BRESTADM


BRESTADM_AUTH     = get_user_auth(BRESTADM)
BRESTADM_SESSION  = OneServer(API_URI, BRESTADM_AUTH)



def test_get_version_by_brestadm():
    one     = One(BRESTADM_SESSION)
    version = one.system.version()
    assert isinstance(version, str), "Полученный объект не является строкой"
