import shutil

RED_COLOR       = "\033[31m"
GREEN_COLOR     = "\033[32m"
DEFAULT_COLOR   = "\033[0m"



def _print_test_result(mehtod_name: str, tes_result: str, result_color_ansi: str ,fill_char='_') -> None:
    terminal_size   = shutil.get_terminal_size()
    terminal_width  = terminal_size.columns
    message_string  = f"{mehtod_name}{fill_char}{tes_result}"
    fill_lenght     = terminal_width - len(message_string)

    if fill_lenght > 0:
        message_string = f"{mehtod_name}{fill_char * fill_lenght}{result_color_ansi}{tes_result}{DEFAULT_COLOR}"
    else:
        message_string = f"{mehtod_name}{fill_char}{result_color_ansi}{tes_result}{DEFAULT_COLOR}"

    print(message_string)



def print_method_fail(mehtod_name: str) -> None:
    _print_test_result(mehtod_name, "FAIL", RED_COLOR)


def print_method_pass(mehtod_name: str) -> None:
    _print_test_result(mehtod_name, "PASS", GREEN_COLOR)
