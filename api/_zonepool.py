from api.one        import OneServer
from pyone.bindings import ZONE_POOLSub



class OneZonepool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_zonepool = one_api.zonepool
    
    
    def info(self) -> ZONE_POOLSub:
        return self._one_zonepool.info()
    