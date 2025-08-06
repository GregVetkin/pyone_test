from api.one        import OneServer
from pyone.bindings import MARKETPLACE_POOLSub



class OneMarketpool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_marketpool = one_api.marketpool
    
    def info(self) -> MARKETPLACE_POOLSub:
        """Retrieves information for all or part of the marketplaces in the pool"""
        return self._one_marketpool.info()
