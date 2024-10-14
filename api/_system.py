from api.one import OneServer
from pyone.bindings import OPENNEBULA_CONFIGURATIONSub



class OneSystem:
    def __init__(self, one_api: OneServer) -> None:
        self._one_system = one_api.system
    
    def version(self) -> str:
        """
        Command: -\n
        XML-RPC Method: one.system.version\n
        Auth. Request: -
        """
        
        return self._one_system.version()
    

    def config(self) -> OPENNEBULA_CONFIGURATIONSub:
        """
        Command: -\n
        XML-RPC Method: one.system.config\n
        Auth. Request: Ony for users in the oneadmin group
        """

        return self._one_system.config()
    