import os
import sys
import subprocess


from utils.printing  import pretty_print_test_result
from utils.commands  import run_command


from config.base    import VENV_DIRECTORY_PATH, PREPARE_SCRIPT_PATH, VENV_PYTHON_3_PATH, TESTS_DIRECTORY_PATH







def run_test(test_path):
    command = f"{VENV_PYTHON_3_PATH} -m pytest \"{test_path}\""

    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode == 0:
        test_is_passed = True
    else:
        test_is_passed = False
    
    return (test_is_passed, result.stdout.decode())
        





if __name__ == "__main__":

    if not os.path.isdir(VENV_DIRECTORY_PATH):
        run_command(f"bash \"{PREPARE_SCRIPT_PATH}\"")

    xmlrpc_method = "one"
    test_function = None

    if len(sys.argv) == 3:
        xmlrpc_method = sys.argv[1]
        test_function = sys.argv[2]

    elif len(sys.argv) == 2:
        xmlrpc_method = sys.argv[1]


    tests_start_dir = xmlrpc_method.split(".")
    tests_start_dir[0] = TESTS_DIRECTORY_PATH

    if len(tests_start_dir) == 3:
        tests_start_dir[2] = f"test_{tests_start_dir[2]}.py"

    test_to_run = "/".join(tests_start_dir)

    if test_function:
        test_to_run = test_to_run + f"::{test_function}"

    test_is_passed, test_output = run_test(test_to_run)

    pretty_print_test_result(xmlrpc_method, test_is_passed)

    if not test_is_passed:
        print(test_output)


