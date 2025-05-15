import pytest
from api        import One
from config     import ADMIN_NAME
from utils      import run_command





@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_get_version(one: One):
    version = one.system.version()
    assert version == run_command("cat /var/lib/one/remotes/VERSION")

