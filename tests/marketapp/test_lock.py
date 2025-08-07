import pytest
import pyone

from api                        import One
from utils.other                import wait_until, get_unic_name
from config.tests               import LOCK_LEVELS

from tests._common_methods.lock import lock__test, not_exist__test






@pytest.fixture(params=LOCK_LEVELS)
def locked_marketapp(one: One, dummy_marketapp: int, request):
    marketapp_id = dummy_marketapp
    lock_level  = request.param

    one.marketapp.lock(marketapp_id, lock_level, False)
    wait_until(lambda: one.marketapp.info(marketapp_id, False).LOCK is not None)

    yield marketapp_id

    one.marketapp.unlock(marketapp_id)
    wait_until(lambda: one.marketapp.info(marketapp_id, False).LOCK is None)



# =================================================================================================
# TESTS
# =================================================================================================





def test_marketapp_not_exist(one: One):
    not_exist__test(one.marketapp)


@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_lock_unlocked(one: One, dummy_marketapp: int, lock_level: int, lock_check: bool):
    marketapp_id = dummy_marketapp

    lock__test(one.marketapp, marketapp_id, lock_level, lock_check)
    one.marketapp.unlock(marketapp_id)



@pytest.mark.parametrize("lock_check", [True, False])
@pytest.mark.parametrize("lock_level", LOCK_LEVELS)
def test_lock_locked(one: One, locked_marketapp: int, lock_level: int, lock_check: bool):
    marketapp_id = locked_marketapp
    lock__test(one.marketapp, marketapp_id, lock_level, lock_check)
