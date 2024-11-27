from api.one        import OneServer
from pyone.bindings import CLUSTERSub




class OneCluster:
    def __init__(self, one_api: OneServer) -> None:
        self._one_cluster = one_api.cluster

    
    def allocate(self, name: str) -> int:
        return self._one_cluster.allocate(name)
    
    def delete(self, cluster_id: int) -> int:
        return self._one_cluster.delete(cluster_id)
    
    def update(self, cluster_id: int, template: str, replace: bool = False) -> int:
        return self._one_cluster.update(cluster_id, template, 0 if replace else 1)
    
    def addhost(self, cluster_id: int, host_id: int) -> int:
        return self._one_cluster.addhost(cluster_id, host_id)
    
    def delhost(self, cluster_id: int, host_id: int) -> int:
        return self._one_cluster.delhost(cluster_id, host_id)
    
    def adddatastore(self, cluster_id: int, datastore_id: int) -> int:
        return self._one_cluster.adddatastore(cluster_id, datastore_id)
    
    def deldatastore(self, cluster_id: int, datastore_id: int) -> int:
        return self._one_cluster.deldatastore(cluster_id, datastore_id)
    
    def addvnet(self, cluster_id: int, vnet_id: int) -> int:
        return self._one_cluster.addvnet(cluster_id, vnet_id)
    
    def delvnet(self, cluster_id: int, vnet_id: int) -> int:
        return self._one_cluster.delvnet(cluster_id, vnet_id)
    
    def rename(self, cluster_id: int, new_name: str) -> int:
        return self._one_cluster.rename(cluster_id, new_name)

    def info(self, cluster_id: int, decrypt_secrets: bool = False) -> CLUSTERSub:
        return self._one_cluster.info(cluster_id, decrypt_secrets)
    
    