from pyone          import OneServer
from api._system    import OneSystem


class One():
    def __init__(self, one_server: OneServer) -> None:
        self._one_api   = one_server

        self.system     = OneSystem(self._one_api)
    

