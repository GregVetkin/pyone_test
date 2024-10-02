import pytest
import sys
import subprocess


from utils.printing import pretty_print_test_result


result = subprocess.run(
    [sys.executable, '-m', 'pytest', 'tests/system/test_system_version.py'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

if result.returncode == 0:
    pretty_print_test_result("one.system.version", True)
else:
    pretty_print_test_result("one.system.version", False)
    print(result.stdout.decode())