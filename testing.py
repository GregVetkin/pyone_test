import unittest

from tests.test_one_system_version import TestOneSystemVersion







if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=0).run(unittest.makeSuite(TestOneSystemVersion))
    if result.wasSuccessful():
        print("Все тесты прошли успешно: PASS")
    else:
        print("Один или несколько тестов провалены: FAIL")