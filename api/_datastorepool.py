from api.one        import OneServer
from pyone.bindings import DATASTORE_POOLSub



class OneDatastorepool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_dspool = one_api.datastorepool
    
    def info(self) -> DATASTORE_POOLSub:
        """Retrieves information for all or part of the datastores in the pool"""
        return self._one_dspool.info()
