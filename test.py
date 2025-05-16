import os
import sys
import subprocess
import shutil

from config.base import TESTS_DIRECTORY_PATH, VENV_DIRECTORY_PATH, VENV_PYTHON_3_PATH, PREPARE_SCRIPT_PATH




def method_to_test_path(method_name: str) -> str:
    methods = method_name.split(".")

    if len(methods) == 3:
        return os.path.join(TESTS_DIRECTORY_PATH, f"{methods[1]}/test_{methods[2]}.py")
    elif len(methods) == 2:
        return os.path.join(TESTS_DIRECTORY_PATH, methods[1])
    else:
        return TESTS_DIRECTORY_PATH



def start_test(test_path: str) -> None:
    command = f"{VENV_PYTHON_3_PATH} -m pytest -v {test_path}"
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
    return os.path.isdir(VENV_DIRECTORY_PATH)


def prepare_venv() -> None:
    subprocess.run(["bash", PREPARE_SCRIPT_PATH])



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
