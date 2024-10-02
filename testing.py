import unittest

from tests  import TestOneSystemVersion
from tests  import TestOneSystemConfig




if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.makeSuite(TestOneSystemVersion))
    if result.wasSuccessful():
        print("Все тесты прошли успешно: PASS")
    else:
        print("Один или несколько тестов провалены: FAIL")

    result = unittest.TextTestRunner(verbosity=2).run(unittest.makeSuite(TestOneSystemConfig))
    if result.wasSuccessful():
        print("Все тесты прошли успешно: PASS")
    else:
        print("Один или несколько тестов провалены: FAIL")