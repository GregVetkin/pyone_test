from config         import COMMAND_EXECUTOR
from utils          import run_command



def _create(function_name: str, template: str) -> int:
    file = "/tmp/test_template_file"

    if "ssh" in COMMAND_EXECUTOR:
        run_command(COMMAND_EXECUTOR + " " + f"\'cat <<EOF > {file}\n{template}\nEOF\'")
    else:
        run_command(COMMAND_EXECUTOR + " " + f"cat <<EOF > {file}\n{template}\nEOF")

    _id = int(run_command(COMMAND_EXECUTOR + " " + f"{function_name} create {file}" + " | awk '{print $2}'"))
    run_command(COMMAND_EXECUTOR + " " + f"rm -f {file}")

    return _id


def _exist(function_name: str, object_id: int) -> bool:
    exec_code_show = int(run_command(COMMAND_EXECUTOR + " " + f"{function_name} show {object_id} &>/dev/null; echo $?"))
    exec_code_list = int(run_command(COMMAND_EXECUTOR + " " + f"{function_name} list | " + "awk '{print $1}' | " + f" grep {object_id} &>/dev/null; echo $?"))
    return True if exec_code_show == 0 and exec_code_list == 0 else False


def _chown(function_name: str, object_id: int, user_id: int, group_id: int = -1) -> None:
    group = group_id if group_id != -1 else ''
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} chown {object_id} {user_id} {group}")


def _chmod(function_name: str, object_id: int, octet: str) -> None:
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} chmod {object_id} {octet}")


def _info(function_name: str, object_id: int, xml: bool = False) -> str:
    xml_flag = "-x" if xml else ""
    return run_command(COMMAND_EXECUTOR + " " + f"{function_name} show {object_id} {xml_flag}")


def _delete(function_name: str, object_id: int) -> None:
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} delete {object_id}")


def _update(function_name: str, object_id: int, template: str, append: bool = False) -> None:
    file = "/tmp/test_file"

    if "ssh" in COMMAND_EXECUTOR:
        run_command(COMMAND_EXECUTOR + " " + f"\'cat <<EOF > {file}\n{template}\nEOF\'")
    else:
        run_command(COMMAND_EXECUTOR + " " + f"cat <<EOF > {file}\n{template}\nEOF")

    append_flag = "-a" if append else ""

    run_command(COMMAND_EXECUTOR + " " + f"{function_name} update {object_id} {file} {append_flag}")
    run_command(COMMAND_EXECUTOR + " " + f"rm -f {file}")


def _lock(function_name: str, object_id: int, lock_level: int = 4) -> None:
    lock_flag = {
            1: "--use",
            2: "--manage",
            3: "--admin",
            4: "--all",
        }
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} lock {object_id} {lock_flag[lock_level]}")


def _unlock(function_name: str, object_id: int) -> None:
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} unlock {object_id}")


def _disable(function_name: str, object_id: int) -> None:
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} disable {object_id}")


def _enable(function_name: str, object_id: int) -> None:
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} enable {object_id}")


def _persistent(function_name: str, object_id: int) -> None:
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} persistent {object_id}")


def _nonpersistent(function_name: str, object_id: int) -> None:
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} nonpersistent {object_id}")


def _rename(function_name: str, object_id: int, new_name: str) -> None:
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} rename {object_id} {new_name}")


def _enable(function_name: str, object_id: int) -> None:
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} enable {object_id}")


def _disable(function_name: str, object_id: int) -> None:
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} disable {object_id}")


def _offline(function_name: str, object_id: int) -> None:
    run_command(COMMAND_EXECUTOR + " " + f"{function_name} offline {object_id}")