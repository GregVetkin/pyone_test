import pytest
from api                import One
from config             import ADMIN_NAME






# =================================================================================================
# TESTS
# =================================================================================================


@pytest.mark.parametrize("one", [ADMIN_NAME], indirect=True)
def test_zone_raft_status(one: One):
    raft_status = one.zone.raftstatus()
    assert raft_status.has__content()



