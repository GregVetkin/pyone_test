from data   import MethodInfo
from pyone  import OneServer



class ApiConnection():
    def __init__(self, uri: str, session: str) -> None:
        self._connection = OneServer(uri=uri, session=session)

    

class Method():
    def __init__(self, api: ApiConnection, method_info: MethodInfo) -> None:
        self.method_info  = method_info
        self._api         = api._connection

    


