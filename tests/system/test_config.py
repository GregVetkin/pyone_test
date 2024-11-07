import pytest

from api        import One
from utils      import get_user_auth
from config     import BRESTADM

BRESTADM_AUTH = get_user_auth(BRESTADM)




@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_get_config(one: One):
    config  = one.system.config()
    assert config.has__content() == True
