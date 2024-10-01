import subprocess


def _run_command(command: str) -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"



def create_user(name: str, password: str, group="brestusers", driver="public") -> str:
    command = f"sudo -u brestadm oneuser create {name} {password} --group {group} --driver {driver}"
    return _run_command(command)


def create_user_token(user: str, group="brestusers") -> str:
    command = f"sudo -u brestadm oneuser token-create {user}"
    
    if group:
        command += f" --group {group}"

    return _run_command(command)


def delete_user(name: str) -> str:
    command = f"sudo -u brestadm oneuser delete {name}"
    return _run_command(command)


if __name__ == "__main__":
    pass
    # user = "test_public_user"
    # result = create_user(user, "12345678")
    # print(result)
    # session = create_user_token(user)
    # print(session)
    # del_user = delete_user(user)
    # print(del_user)