from one_cli.zone._common       import ZoneInfo, parse_zone_info_from_xml
from one_cli._base_commands     import _chmod, _chown, _delete, _info, _update, _exist, _create
from one_cli.image              import force_delete_image

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


    def info(self) -> ZoneInfo:
        return parse_zone_info_from_xml(_info(self._function, self._id, xml=True))


    def update(self, template: str, append: bool = False) -> None:
        _update(self._function, self._id, template, append)

