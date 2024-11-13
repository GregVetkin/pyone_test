from api.one        import OneServer
from pyone.bindings import VMTEMPLATE_POOLSub



class OneTemplatepool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_templatepool = one_api.templatepool
    
    def info(self, filter_flag: int = -2, start_id: int = -1, end_id: int = -1) -> VMTEMPLATE_POOLSub:
        return self._one_templatepool.info(filter_flag, start_id, end_id)
    
    