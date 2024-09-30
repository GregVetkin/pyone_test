import unittest
from pyone  import OneServer
from api    import One



class TestOneSystemVersion(unittest.TestCase):

    def setUp(self):
        # Подключение к реальной OpenNebula среде перед каждым тестом
        self.server_url = 'http://bufn1.brest.local:2633/RPC2'
        self.username   = 'test_user'
        self.token      = 'test_token'
        self.one        = One(OneServer(self.server_url, session=f'{self.username}:{self.token}'))
        
        # Уникальная подготовка для каждого теста, основываясь на его имени
        if self._testMethodName == "test_case_1":
            # Подготовка для первого теста
            print("Подготовка для test_case_1...")
            # Например, создание тестовой сущности или установка конфигурации
            self.setup_test_case_1()
        
        elif self._testMethodName == "test_case_2":
            # Подготовка для второго теста
            print("Подготовка для test_case_2...")
            # Например, другое действие для подготовки
            self.setup_test_case_2()

    def tearDown(self):
        # Возврат системы в нормальное состояние после каждого теста
        if self._testMethodName == "test_case_1":
            # Очистка после первого теста
            print("Очистка после test_case_1...")
            self.cleanup_test_case_1()
        
        elif self._testMethodName == "test_case_2":
            # Очистка после второго теста
            print("Очистка после test_case_2...")
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
            print("Выполнение test_case_1...")
            version = self.one.system.version()
            self.assertIsInstance(version, str, msg="Ошибка: Версия должна быть строкой.")

            # Проверка формата версии
            version_parts = version.split('.')
            self.assertEqual(len(version_parts), 3, msg="Ошибка: Неверный формат версии.")
            self.assertTrue(all(part.isdigit() for part in version_parts), msg="Ошибка: Части версии должны быть числами.")
            
            print("test_case_1____PASS")
        except AssertionError as e:
            print("test_case_1____FAIL")
            print(f"Причина: {e}")
            raise

    def test_case_2(self):
        pass

if __name__ == '__main__':
    # Запускаем тесты и отслеживаем результат
    result = unittest.TextTestRunner(verbosity=2).run(unittest.makeSuite(TestOneSystemVersion))
    if result.wasSuccessful():
        print("Все тесты прошли успешно: PASS")
    else:
        print("Один или несколько тестов провалены: FAIL")
