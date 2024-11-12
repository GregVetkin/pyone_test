from api.one        import OneServer
from pyone.bindings import HOST_POOLSub



class OneHostpool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_hostpool = one_api.hostpool
    
    
    def info(self) -> HOST_POOLSub:
        return self._one_hostpool.info()
    

    def monitoring(self, last_seconds: int = -1):
        return self._one_hostpool.monitoring(last_seconds)