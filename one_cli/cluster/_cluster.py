from utils                      import run_command
from one_cli._base_commands     import _chmod, _chown, _delete, _info, _update, _exist
from one_cli.cluster._common    import ClusterInfo, parse_cluster_info_from_xml

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

    def update(self, template: str, append: bool = False) -> None:
        _update(self._function, self._id, template, append)

    def info(self) -> ClusterInfo:
        return parse_cluster_info_from_xml(_info(self._function, self._id, xml=True))
    
    
    def adddatastore(self, datastore_id: int) -> None:
        run_command(f"sudo {self._function} adddatastore {self._id} {datastore_id}")
    
    def deldatastore(self, datastore_id: int) -> None:
        run_command(f"sudo {self._function} deldatastore {self._id} {datastore_id}")

    def addhost(self, host_id: int) -> None:
        run_command(f"sudo {self._function} addhost {self._id} {host_id}")
    
    def delhost(self, host_id: int) -> None:
        run_command(f"sudo {self._function} delhost {self._id} {host_id}")

    def addvnet(self, vnet_id: int) -> None:
        run_command(f"sudo {self._function} addvnet {self._id} {vnet_id}")
    
    def delvnet(self, vnet_id: int) -> None:
        run_command(f"sudo {self._function} delvnet {self._id} {vnet_id}")
