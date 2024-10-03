import os

FAIL        = "FAIL"
PASS        = "PASS"
RED_FAIL    = f"\033[1;31m{FAIL}\033[0m"
GREEN_PASS  = f"\033[1;32m{PASS}\033[0m"



def pretty_print_test_result(test_name: str, test_passed: bool, fillet="_") -> None:
    test_result     = PASS if test_passed else FAIL

    terminal_lenght = os.get_terminal_size().columns
    total_length    = len(test_name) + len(test_result)
    fill_length     = terminal_lenght - total_length

    if fill_length < 1:
        fill_length = 1
    
    on_print = f"{test_name}{fillet * fill_length}{GREEN_PASS if test_passed else RED_FAIL}"
    print(on_print)



if __name__ == "__main__":
    pretty_print_test_result("one.system.config", True)
    pretty_print_test_result("one.system.version", False)
    pretty_print_test_result("one.onevm.action", True, "-")