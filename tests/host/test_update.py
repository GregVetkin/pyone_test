import pytest
from api                            import One
from tests._common_methods.update   import update__test, not_exist__test






def test_host_not_exist(one: One):
    not_exist__test(one.host)


@pytest.mark.parametrize("update_type", [0, 1])
def test_update_type(one: One, dummy_host: int, update_type: int):
    host_id = dummy_host
    update__test(one.host, host_id, update_type)