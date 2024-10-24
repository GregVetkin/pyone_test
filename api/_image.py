from api.one import OneServer

class OneImage:
    def __init__(self, one_api: OneServer) -> None:
        self._one_image = one_api.image
    
    def allocate(self, template: str, storage_id: int, check_storage_capacity: bool = True) -> int:
        return self._one_image.allocate(template, storage_id, check_storage_capacity)
    

