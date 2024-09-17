from api    import OneSystemVersion
from utils  import print_method_fail, print_method_pass, create_user_token, remove_all_user_tokens
from tests  import TestMethod


# Testing one.server.version


class TestOneSystemVersion(TestMethod):
    
    def test(self):
        pass


    def _test_no_group(self):
        user = "brestadm"

        remove_all_user_tokens(user)
        create_user_token(user, "")
        remove_all_user_tokens(user)

    def _test_bretusers_group(self):
        pass
    
    def _test_brestadmins_group(self):
        pass


