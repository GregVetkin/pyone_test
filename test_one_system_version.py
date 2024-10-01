import unittest

from pyone  import OneServer
from api    import One


class TestOneSystemVersion(unittest.TestCase):

    def setUp(self):
        self.server_url = 'http://bufn1.brest.local:2633/RPC2'
        self.username   = 'tester'
        self.token      = '1d9cf00e958b9f6ac7d4472e24a2ecaa1f9ee9e862958f8ae04477542e4e466c'
        self.one        = One(OneServer(self.server_url, session=f'{self.username}:{self.token}'))
        
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
        # Уникальные подготовительные действия для test_case_1
        pass

    def cleanup_test_case_1(self):
        # Уникальные послетестовые действия для test_case_1
        pass

    def setup_test_case_2(self):
        # Уникальные подготовительные действия для test_case_2
        pass

    def cleanup_test_case_2(self):
        # Уникальные послетестовые действия для test_case_2
        pass

    def test_case_1(self):
        try:
            # Выполнение первого теста
            version = self.one.system.version()
            self.assertIsInstance(version, str, msg="Ошибка: Версия должна быть строкой.")

            # Проверка формата версии
            version_parts = version.split('.')
            self.assertTrue(all(part.isdigit() for part in version_parts), msg="Ошибка: Части версии должны быть числами.")
            

        except AssertionError as e:
            print("test_case_1____FAIL")
            print(f"Причина: {e}")
            raise

    def test_case_2(self):
        pass

if __name__ == '__main__':
    # Запускаем тесты и отслеживаем результат
    result = unittest.TextTestRunner(verbosity=0).run(unittest.makeSuite(TestOneSystemVersion))
    if result.wasSuccessful():
        print("Все тесты прошли успешно: PASS")
    else:
        print("Один или несколько тестов провалены: FAIL")
