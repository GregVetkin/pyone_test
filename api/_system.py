from api.one import OneServer
from pyone.bindings import OPENNEBULA_CONFIGURATIONSub



class OneSystem:
    def __init__(self, one_api: OneServer) -> None:
        self._one_system = one_api.system
    
    def version(self) -> str:
        """Returns the OpenNebula core version"""
        return self._one_system.version()
    
    def config(self) -> OPENNEBULA_CONFIGURATIONSub:
        """Returns the OpenNebula configuration"""
        return self._one_system.config()
