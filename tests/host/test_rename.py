import pytest

from api                        import One
from utils                      import get_unic_name
from one_cli.host               import Host, create_host, host_exist
from config                     import ADMIN_NAME, BAD_SYMBOLS

from tests._common_tests.rename import rename__test
from tests._common_tests.rename import rename_if_not_exist__test
from tests._common_tests.rename import rename_unavailable_symbol__test
from tests._common_tests.rename import rename_empty_name__test
from tests._common_tests.rename import rename_collision__test





@pytest.fixture
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def host(one: One):
    host_id = one.host.allocate(f"{get_unic_name()}")
    host    = Host(host_id)
    yield host
    if host_exist(host_id):
        host.delete()
    


@pytest.fixture
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def host_2(one: One):
    host_id = one.host.allocate(f"{get_unic_name()}")
    host    = Host(host_id)
    yield host
    if host_exist(host_id):
        host.delete()



# =================================================================================================
# TESTS
# =================================================================================================



@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_not_exist(one: One):
    rename_if_not_exist__test(one.host)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_rename_host(one: One, host: Host):
    rename__test(one.host, host)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_host_name_collision(one: One, host: Host, host_2: Host):
    rename_collision__test(one.host, host, host_2)


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_empty_host_name(one: One, host: Host):
    rename_empty_name__test(one.host, host)


@pytest.mark.parametrize("bad_symbol", BAD_SYMBOLS)
@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_unavailable_symbols_in_host_name(one: One, host: Host, bad_symbol: str):
    rename_unavailable_symbol__test(one.host, host, bad_symbol)

