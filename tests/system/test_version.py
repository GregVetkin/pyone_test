import pytest

from api        import One
from utils      import get_user_auth
from config     import BRESTADM

BRESTADM_AUTH = get_user_auth(BRESTADM)




@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_get_version(one: One):
    version = one.system.version()
    assert isinstance(version, str), "Полученный объект не является строкой"

