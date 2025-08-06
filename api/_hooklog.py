from api.one        import OneServer
from pyone.bindings import HISTORY_RECORDSSub



class OneHooklog:
    def __init__(self, one_api: OneServer) -> None:
        self._one_hooklog = one_api.hooklog

    def info(self, min_date: int, max_date: int, hook_id: int, execution_code: int) -> HISTORY_RECORDSSub:
        """Retrieves information from the hook execution log"""
        return self._one_hooklog.info(min_date, max_date, hook_id, execution_code)