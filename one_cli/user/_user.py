from config     import COMMAND_EXECUTOR
from utils      import run_command



def create_user(name: str, password: str = "12345678", driver: str = "public"):
    return int(run_command(COMMAND_EXECUTOR + " " + f"oneuser create {name} {password}, --driver {driver} " + " | awk '{print $2}'"))



class User:
    def __init__(self, user_id: int) -> None:
        self._id = user_id

    def delete(self) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"oneuser delete {self._id}")

