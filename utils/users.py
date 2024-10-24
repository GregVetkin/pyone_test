from utils  import run_command

RUN_FROM_BRESTADM = "sudo -u brestadm"



# def create_user(name: str, password: str, group="brestusers", driver="public") -> str:
#     command = f"{RUN_FROM_BRESTADM} oneuser create {name} {password} --group {group} --driver {driver}"
#     return run_command(command)


# def create_user_token(user: str, group: str) -> str:
#     command = f"{RUN_FROM_BRESTADM} oneuser token-create {user} --group {group}"
#     return run_command(command)


# def delete_user(name: str) -> str:
#     command = f"{RUN_FROM_BRESTADM} oneuser delete {name}"
#     return run_command(command)




def get_brestadm_auth() -> str:
    command = "sudo cat /var/lib/one/homes/brestadm/one_auth"
    return run_command(command)





if __name__ == "__main__":
    pass
