import pyone
import pytest

from api            import One
# from utils.users    import get_api_connection_by_user_id




# @pytest.fixture
# def brestusers_user(one: One):
#     user_id = one.user.allocate("testes", "12345678")
#     one.user.login("testes", period=36000, group_id=1)
#     yield user_id




def test_get_config(one: One):
    config = one.system.config()
    assert config.has__content()



# def test_only_admin_group(brestusers_user):
#     one = One(get_api_connection_by_user_id(brestusers_user))

#     with pytest.raises(pyone.OneAuthorizationException):
#         one.system.config()