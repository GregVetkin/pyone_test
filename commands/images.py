from utils  import run_command



def get_image_type(image_id: int) -> str:
    command = f"sudo oneimage show {image_id} | grep TYPE | head -n 1 " + " | awk '{printf $3}'"
    return run_command(command)

