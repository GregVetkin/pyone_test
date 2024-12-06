from dataclasses                import dataclass
from one_cli._base_commands     import _delete, _info_dataclass, _update, _exist, _create



FUNCTION_NAME = "onezone"




def zone_exist(zone_id: int) -> bool:
    return _exist(FUNCTION_NAME, zone_id)


def create_zone(zone_template: str) -> int:
    return _create(FUNCTION_NAME, zone_template)





class Zone:
    def __init__(self, zone_id: int) -> None:
        self._id        = zone_id
        self._function  = FUNCTION_NAME
    
    def delete(self) -> None:
        _delete(self._function, self._id)


    def info(self) -> dataclass:
        return _info_dataclass(self._function, self._id)


    def update(self, template: str, append: bool = False) -> None:
        _update(self._function, self._id, template, append)

