import unittest

from pyone  import OneServer, OneAuthorizationException
from api    import One
from utils  import create_user, create_user_token, delete_user




class TestOneSystemConfig(unittest.TestCase):

    def setUp(self):
        self.server_url = 'http://bufn1.brest.local:2633/RPC2'
        self.user       = "tester"
        self.password   = "12345678"

        if self._testMethodName == "test_case_1":
            self.group  = "brestusers"

        elif self._testMethodName == "test_case_2":
            self.group  = "brestadmins"

        create_user(self.user, self.password, self.group)
        self.session    = create_user_token(self.user, self.group)
        self.one        = One(OneServer(self.server_url, self.session))


    def tearDown(self):
        delete_user(self.user)


    def test_case_1(self):
        try:
            self.assertRaises(OneAuthorizationException, self.one.system.config)

        except AssertionError as e:
            print(f"Провален тест для группы {self.group}")
            print(f"Ошибка: пользователь из неадминистративной группы brestusers имеет доступ к конфигурации")
            raise

    def test_case_2(self):
        try:
            self.one.system.config()

        except Exception as e:
            print(f"Провален тест для группы {self.group}")
            print(f"Причина: {e}")
            raise



if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.makeSuite(TestOneSystemConfig))
    if result.wasSuccessful():
        print("Все тесты прошли успешно: PASS")
    else:
        print("Один или несколько тестов провалены: FAIL")
