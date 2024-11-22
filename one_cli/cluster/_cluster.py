from utils                  import run_command
from one_cli._base_commands import _chmod, _chown, _delete, _info, _update, _exist


FUNCTION_NAME = "onecluster"


def create_cluster(name: str):
    return int(run_command(f"sudo {FUNCTION_NAME} create {name}" + " | awk '{print $2}'"))


def cluster_exist(cluster_id: int) -> bool:
    return _exist(FUNCTION_NAME, cluster_id)




class Cluster:
    def __init__(self, cluster_id: int) -> None:
        self._id        = cluster_id
        self._function  = FUNCTION_NAME

    def delete(self) -> None:
        _delete(self._function, self._id)


