from api.one        import OneServer
from pyone.bindings import HOST_POOLSub



class OneHostpool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_hostpool = one_api.hostpool
    
    
    def info(self) -> HOST_POOLSub:
        """Retrieves information for all the hosts in the pool"""
        return self._one_hostpool.info()
    

    def monitoring(self, last_seconds: int = -1):
        """Returns all the host monitoring records"""
        return self._one_hostpool.monitoring(last_seconds)
