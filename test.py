import sys
import subprocess
import os

from tests              import TestData
from utils.printing     import pretty_print_test_result
from _tests             import TESTS




def run_test(test: TestData) -> None:
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', test.test_file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode == 0:
        test_passed = True
    else:
        test_passed = False
        print(result.stdout.decode())
    
    pretty_print_test_result(test.xml_rpc_method, test_passed)
        



if __name__ == "__main__":
    if len(sys.argv) > 1:
        method = sys.argv[1]
    else:
        method = "one"

    l = method.split(".")

    test = TestData(
        xml_rpc_method  =   "one.system.version",
        test_file_path  =   "/home/gregory/Документы/Projects/pyone_test/tests/system/test_version.py",
        cli_command     =   "-"
    )

    run_test(test)