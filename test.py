import os
import sys
import subprocess

from tests              import TestData
from _tests             import TESTS, PROJECT_DIR
from utils.printing     import pretty_print_test_result
from utils              import run_command




def dfs_tests(test_tree, dotted_key):
    keys = dotted_key.split(".")
    node = test_tree

    for key in keys:
        if key in node:
             node = node[key]
        else:
            print("Method not found")
            return
    

    def _dfs(node, current_path):
        if isinstance(node, dict):
            for key, value in node.items():
                yield from _dfs(value, current_path + [key])
        else:
            yield node

    yield from _dfs(node, keys)




def run_test(test: TestData) -> None:
    command = f"{PROJECT_DIR}/.venv/bin/python3 -m pytest {test.test_file_path}"

    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode == 0:
        test_passed = True
    else:
        test_passed = False
        print(result.stdout.decode())
    
    pretty_print_test_result(test.xml_rpc_method, test_passed)
        


def venv_exist() -> bool:
    return os.path.isdir(os.path.join(PROJECT_DIR, '.venv'))


def prepare_venv() -> None:
    prepare_script_path = os.path.join(PROJECT_DIR, "prepare.sh")
    subprocess.run(["bash", prepare_script_path], stdin=None, stdout=None)


if __name__ == "__main__":
    if not venv_exist():
        prepare_venv()

    if len(sys.argv) > 1:
        method = sys.argv[1]
    else:
        method = "one"

    for test in dfs_tests(TESTS, method):
        run_test(test)
