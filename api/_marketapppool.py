from api.one        import OneServer
from pyone.bindings import MARKETPLACEAPP_POOLSub



class OneMarketapppool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_marketapppool = one_api.marketapppool
    
    def info(self, filter_flag: int, start_id: int, end_id: int) -> MARKETPLACEAPP_POOLSub:
        """Retrieves information for all or part of the marketplace apps in the pool"""
        return self._one_marketapppool.info(filter_flag, start_id, end_id)
