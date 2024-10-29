import os
from utils  import run_command
from time   import sleep


def create_image_by_tempalte(datastore_id: int, image_template: str, await_image_rdy: bool = True) -> int:
    template_file_path  = "/tmp/test_template_file"

    with open(template_file_path, "w") as template_file:
        template_file.write(image_template)
    
    command     = f"sudo oneimage create -d {datastore_id} {template_file_path}" + " | awk '{print $2}'"
    image_id    = int(run_command(command))

    if await_image_rdy:
        wait_image_rdy(image_id)
        
    os.remove(template_file_path)
    return image_id


def is_image_exist(image_id: int) -> bool:
    command     = f"sudo oneimage show {image_id} &>/dev/null; echo $?"
    exec_code   = int(run_command(command))
    return True if exec_code == 0 else False


def delete_image(image_id: int) -> None:
    command = f"sudo oneimage delete {image_id}"
    run_command(command)


def wait_image_rdy(image_id: int, check_interval: float = 1.0) -> None:
    while True:
        if get_image_state(image_id) == "rdy":
            break
        else:
            sleep(check_interval)


def get_image_state(image_id: int) -> str:
    command = f"sudo oneimage show {image_id} | grep STATE | head -n 1 " + " | awk '{print $3}'"
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

