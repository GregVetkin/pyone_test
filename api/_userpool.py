from api.one        import OneServer
from pyone.bindings import USER_POOLSub



class OneUserpool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_userpool = one_api.userpool
    
    def info(self) -> USER_POOLSub:
        """Retrieves information for all the users in the pool"""
        return self._one_userpool.info()
