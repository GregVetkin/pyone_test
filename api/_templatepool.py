from api.one        import OneServer
from pyone.bindings import VMTEMPLATE_POOLSub



class OneTemplatepool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_templatepool = one_api.templatepool
    
    def info(self, filter_flag: int, start_id: int, end_id: int) -> VMTEMPLATE_POOLSub:
        """Retrieves information for all or part of the Resources in the pool"""
        return self._one_templatepool.info(filter_flag, start_id, end_id)
