from api.one        import OneServer
from pyone.bindings import DATASTORE_POOLSub



class OneDatastorepool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_dspool = one_api.datastorepool
    
    def info(self) -> DATASTORE_POOLSub:
        return self._one_dspool.info()