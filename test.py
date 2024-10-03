import sys
import subprocess
import os

from tests              import TestData
from utils.printing     import pretty_print_test_result
from _tests             import TESTS, PROJECT_DIR



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
    command = f"source {PROJECT_DIR}/.venv/bin/activate && python3 -m pytest {test.test_file_path} ; deactivate"
    
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
        



if __name__ == "__main__":
    if len(sys.argv) > 1:
        method = sys.argv[1]
    else:
        method = "one"


    method = "one.system"   # for now
    for test in dfs_tests(TESTS, method):
        run_test(test)
