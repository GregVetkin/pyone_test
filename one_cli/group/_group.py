from config     import COMMAND_EXECUTOR
from utils      import run_command



def create_group(name: str):
    return int(run_command(COMMAND_EXECUTOR + " " + f"onegroup create {name}" + " | awk '{print $2}'"))



class Group:
    def __init__(self, group_id: int) -> None:
        self._id = group_id

    def delete(self) -> None:
        run_command(COMMAND_EXECUTOR + " " + f"onegroup delete {self._id}")

