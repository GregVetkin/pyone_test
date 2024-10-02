import pytest
import sys
import subprocess
import os

from utils.printing     import pretty_print_test_result
from _tests             import TESTS



current_directory = os.path.dirname(os.path.abspath(__file__))


result = subprocess.run(
    [sys.executable, '-m', 'pytest', f'{current_directory}/{TESTS["one"]["system"]["version"]}'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)


if result.returncode == 0:
    pretty_print_test_result("one.system.version", True)
else:
    pretty_print_test_result("one.system.version", False)
    print(result.stdout.decode())