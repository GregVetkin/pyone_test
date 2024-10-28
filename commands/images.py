from utils  import run_command



def get_image_type(image_id: int) -> str:
    command = f"sudo oneimage show {image_id} | grep TYPE | head -n 1 " + " | awk '{printf $3}'"
    return run_command(command)


def get_image_user(image_id: int) -> str:
    command = f"sudo oneimage show {image_id} | grep USER | head -n 1 " + " | awk '{print $3}'"
    return run_command(command)


def get_image_group(image_id: int) -> str:
    command = ""
    return run_command(command)