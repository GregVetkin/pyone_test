from api.one        import OneServer
from pyone.bindings import HOOK_POOLSub



class OneHookpool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_hookpool = one_api.hookpool
    
    def info(self, filter_flag: int, start_id: int, end_id: int) -> HOOK_POOLSub:
        """Retrieves information for all or part of the Resources in the pool"""
        return self._one_hookpool.info(filter_flag, start_id, end_id)
