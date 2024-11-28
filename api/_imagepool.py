from api.one        import OneServer
from pyone.bindings import IMAGE_POOLSub



class OneImagepool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_imagepool = one_api.imagepool
    
    def info(self, filter_flag: int = -2, start_id: int = -1, end_id: int = -1) -> IMAGE_POOLSub:
        """Retrieves information for all or part of the images in the pool"""
        return self._one_imagepool.info(filter_flag, start_id, end_id)
