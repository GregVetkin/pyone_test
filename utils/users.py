import subprocess

RUN_FROM_BRESTADM = "sudo -u brestadm"


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
        print(f"{e.stderr}")
        raise
        



def create_user(name: str, password: str, group="brestusers", driver="public") -> str:
    command = f"{RUN_FROM_BRESTADM} oneuser create {name} {password} --group {group} --driver {driver}"
    return _run_command(command)


def create_user_token(user: str, group: str) -> str:
    command = f"{RUN_FROM_BRESTADM} oneuser token-create {user} --group {group}"
    return _run_command(command)


def delete_user(name: str) -> str:
    command = f"{RUN_FROM_BRESTADM} oneuser delete {name}"
    return _run_command(command)


if __name__ == "__main__":
    pass
    user = "test_public_user"
    result = create_user(user, "12345678")
    # print(result)
    # session = create_user_token(user)
    # print(session)
    # del_user = delete_user(user)
    # print(del_user)