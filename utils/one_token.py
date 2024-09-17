import subprocess

def create_user_token(username:str, group="", exp_time=3600) -> str:

    command = ["sudo", "oneuser", "token-create", username, "--time", exp_time]

    if group:
        command.append("--group")
        command.append(group)
    

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )

    except subprocess.CalledProcessError as err:
        print(err.stderr.strip())
        exit(1)
    else:
        return result.stdout.strip()



def remove_all_user_tokens(username:str) -> None:
    try:
        command_exec = subprocess.run(
            ["sudo", "oneuser", "token-delete-all", username],
            check=True,
            shell=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as err:
        print(f"Удаление токенов для {username} завершилось неудачей:", err.stderr.strip())
        exit(1)

