from api.one        import OneServer
from pyone.bindings import GROUP_POOLSub



class OneGrouppool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_grouppool = one_api.grouppool
    
    def info(self) -> GROUP_POOLSub:
        """Retrieves information for all the groups in the pool"""
        return self._one_grouppool.info()