import pytest

from api           import One
from utils         import get_user_auth
from one_cli.host  import Host, create_host, host_exist
from config        import BRESTADM

from tests._common_tests.delete import delete__test
from tests._common_tests.delete import delete_if_not_exist__test
from tests._common_tests.delete import delete_undeletable__test

BRESTADM_AUTH = get_user_auth(BRESTADM)


@pytest.fixture
@pytest.mark.parametrize("one", [BRESTADM_AUTH,], indirect=True)
def host(one: One):
    host_id = one.host.allocate("api_test_host_delete")
    host    = Host(host_id)
    yield host
    if host_exist(host_id):
        host.delete()



# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_host_not_exist(one: One):
   delete_if_not_exist__test(one.host)
   

@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_delete_host(one: One, host: Host):
    delete__test(one.host, host)


@pytest.mark.skip(reason="Сделать тест(фикстуру хоста с вм). Добавить классу вм метод миграции. Проверить возможна ли миграция на хост в статусе err")
@pytest.mark.parametrize("one", [BRESTADM_AUTH], indirect=True)
def test_delete_host_with_vm(one: One, host: Host):
    delete_undeletable__test(one.host, host)
