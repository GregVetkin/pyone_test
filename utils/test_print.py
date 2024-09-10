

RED_COLOR       = "\033[31m"
GREEN_COLOR     = "\033[32m"
DEFAULT_COLOR   = "\033[0m"



def _print_method(mehtod_name: str) -> None:
    print(mehtod_name, "________", end="")


def print_method_fail(mehtod_name: str) -> None:
    _print_method(mehtod_name)
    print(RED_COLOR, "FAIL", DEFAULT_COLOR)


def print_method_pass(mehtod_name: str) -> None:
    _print_method(mehtod_name)
    print(GREEN_COLOR, "PASS", DEFAULT_COLOR)