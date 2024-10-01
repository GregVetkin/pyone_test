import unittest

from pyone  import OneServer
from api    import One
from utils  import create_user, create_user_token, delete_user


class TestOneSystemVersion(unittest.TestCase):

    def setUp(self):
        self.server_url = 'http://bufn1.brest.local:2633/RPC2'

        if self._testMethodName == "test_case_1":
            self.setup_test_case_1()
        
        elif self._testMethodName == "test_case_2":
            self.setup_test_case_2()

    def tearDown(self):
        if self._testMethodName == "test_case_1":
            self.cleanup_test_case_1()
        
        elif self._testMethodName == "test_case_2":
            self.cleanup_test_case_2()

    def setup_test_case_1(self):
        self.user       = "tester"
        self.password   = "12345678"
        self.group      = "brestusers"

        create_user(self.user, self.password, self.group)
        self.session    = create_user_token(self.user, self.group)
        self.one        = One(OneServer(self.server_url, self.session))

    def cleanup_test_case_1(self):
        delete_user(self.user)

    def setup_test_case_2(self):
        self.user       = "tester_admin"
        self.password   = "12345678"
        self.group      = "brestadmins"

        create_user(self.user, self.password, self.group)
        
        self.session    = create_user_token(self.user, self.group)
        self.one        = One(OneServer(self.server_url, self.session))

    def cleanup_test_case_2(self):
        delete_user(self.user)

    def test_case_1(self):
        try:
            version = self.one.system.version()
            self.assertIsInstance(version, str, msg="Ошибка: Версия должна быть строкой.")

            version_parts = version.split('.')
            self.assertTrue(all(part.isdigit() for part in version_parts), msg="Ошибка: Части версии должны быть числами.")

        except AssertionError as e:
            print("test_case_1____FAIL")
            print(f"Причина: {e}")
            raise

    def test_case_2(self):
        try:
            version = self.one.system.version()
            self.assertIsInstance(version, str, msg="Ошибка: Версия должна быть строкой.")

            version_parts = version.split('.')
            self.assertTrue(all(part.isdigit() for part in version_parts), msg="Ошибка: Части версии должны быть числами.")
            
        except AssertionError as e:
            print("test_case_1____FAIL")
            print(f"Причина: {e}")
            raise

if __name__ == '__main__':
    # Запускаем тесты и отслеживаем результат

    result = unittest.TextTestRunner(verbosity=2).run(unittest.makeSuite(TestOneSystemVersion))
    if result.wasSuccessful():
        print("Все тесты прошли успешно: PASS")
    else:
        print("Один или несколько тестов провалены: FAIL")
