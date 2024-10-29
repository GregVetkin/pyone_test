from utils  import run_command



def get_user_id_by_name(user_name: str) -> int:
    command = "sudo oneuser list | awk '{print $1 \" \" $2}' " + f" | grep {user_name} " + " | awk '{print $1}'"
    return int(run_command(command))
