from utils  import run_command



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

