from utils  import run_command
from time   import sleep

def is_image_exist(image_id: int) -> bool:
    command     = f"sudo oneimage show {image_id} &>/dev/null; echo $?"
    exec_code   = int(run_command(command))
    return True if exec_code == 0 else False


def delete_image(image_id: int) -> None:
    command = f"sudo oneimage delete {image_id}"
    run_command(command)


def wait_image_rdy(image_id: int, check_interval: float = 1.0) -> None:
    while get_image_state(image_id) != "rdy":
        sleep(check_interval)


def get_image_state(image_id: int) -> str:
    command = f"sudo oneimage show {image_id} | grep STATE | head -n 1 " + " awk '{print $3}'"
    return run_command(command)


def get_image_type(image_id: int) -> str:
    command = f"sudo oneimage show {image_id} | grep TYPE | head -n 1 " + " | awk '{printf $3}'"
    return run_command(command)


def get_image_user(image_id: int) -> str:
    command = f"sudo oneimage show {image_id} | grep USER | head -n 1 " + " | awk '{print $3}'"
    return run_command(command)


def get_image_group(image_id: int) -> str:
    command = f"sudo oneimage show {image_id} | grep GROUP | head -n 1 " + " | awk '{print $3}'"
    return run_command(command)


def get_image_user_rights(image_id: int) -> str:
    command = f"sudo oneimage show {image_id} | grep -A 4 PERMISSIONS | grep OWNER " + " | awk '{print $3}'"
    return run_command(command)


def get_image_group_rights(image_id: int) -> str:
    command = f"sudo oneimage show {image_id} | grep -A 4 PERMISSIONS | grep GROUP " + " | awk '{print $3}'"
    return run_command(command)


def get_image_other_rights(image_id: int) -> str:
    command = f"sudo oneimage show {image_id} | grep -A 4 PERMISSIONS | grep OTHER " + " | awk '{print $3}'"
    return run_command(command)

