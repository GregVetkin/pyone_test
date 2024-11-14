from one_cli._base_commands     import _delete, _info, _update, _exist, _rename, _enable, _disable, _offline, _create, _lock, _unlock
from one_cli.template._common   import TemplateInfo, parse_template_info_from_xml


FUNCTION = "onetemplate"



def create_template(vmtemplate: str):
    return _create(FUNCTION, vmtemplate)


def template_exist(template_id: int) -> bool:
    return _exist(FUNCTION, template_id)




class Template:
    def __init__(self, template_id: int) -> None:
        self._id        = template_id
        self._function  = FUNCTION


    def delete(self) -> None:
        _delete(self._function, self._id)


    def rename(self, new_name: str) -> None:
        _rename(self._function, self._id, new_name)


    def info(self) -> TemplateInfo:
        return parse_template_info_from_xml(_info(self._function, self._id, xml=True))
    

    def lock(self, lock_level: int = 4) -> None:
        _lock(self._function, self._id, lock_level)


    def unlock(self) -> None:
        _unlock(self._function, self._id)
