import os
import sys
import subprocess
import shutil

from config import PROJECT_DIR




def method_to_test_path(method_name: str) -> str:
    methods = method_name.split(".")

    if len(methods) == 3:
        tests_relative_path = f"tests/{methods[1]}/test_{methods[2]}.py"
    elif len(methods) == 2:
        tests_relative_path = f"tests/{methods[1]}"
    else:
        tests_relative_path = f"tests"

    test_path = os.path.join(PROJECT_DIR, tests_relative_path)
    return test_path



def start_test(test_path: str) -> None:
    python_interpreter = os.path.join(PROJECT_DIR, ".venv/bin/python3")
    command = f"{python_interpreter} -m pytest -v {test_path}"
    subprocess.run(command, shell=True)


def print_testing_method(method_name: str):
    bold            = "\033[1m"
    orange_color    = "\033[38;5;208m"
    no_color        = "\033[0m"
    terminal_width  = shutil.get_terminal_size().columns
    centered_text   = method_name.center(terminal_width)

    print()
    print(f"{bold}{orange_color}{centered_text}{no_color}")
    print()

        

def venv_exist() -> bool:
    return os.path.isdir(os.path.join(PROJECT_DIR, '.venv'))


def prepare_venv() -> None:
    prepare_script_path = os.path.join(PROJECT_DIR, "prepare.sh")
    subprocess.run(["bash", prepare_script_path], stdin=None, stdout=None)



def clear_terminal() -> None:
    command = 'printf "\\033[0H\\033[$(tput lines)L"'
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    if not venv_exist():
        prepare_venv()

    if len(sys.argv) > 1:
        method = sys.argv[1]
    else:
        method = "one"

    test_path = method_to_test_path(method)

    clear_terminal()
    print_testing_method(method)
    start_test(test_path)
