from api.one        import OneServer
from pyone.bindings import CLUSTER_POOLSub



class OneClusterpool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_clusterpool = one_api.clusterpool
    
    def info(self) -> CLUSTER_POOLSub:
        """Retrieves information for all the clusters in the pool"""
        return self._one_clusterpool.info()
