from config                     import COMMAND_EXECUTOR
from utils                      import run_command
from one_cli.datastore._common  import DatastoreInfo, parse_datastore_info_from_xml
from one_cli._base_commands     import _chmod, _chown, _delete, _info, _update, _exist, _create



def datastore_exist(datastore_id: int) -> bool:
    return _exist("onedatastore", datastore_id)


def create_ds_by_tempalte(ds_template: str) -> int:
    return _create("onedatastore", ds_template)





class Datastore:
    def __init__(self, datastore_id: int) -> None:
        self._id        = datastore_id
        self._function  = "onedatastore"
    
    def delete(self) -> None:
        _delete(self._function, self._id)

    def chmod(self, octet: str) -> None:
        _chmod(self._function, self._id, octet)

    def chown(self, user_id: int, group_id: int = -1) -> None:
        _chown(self._function, self._id, user_id, group_id)

    def info(self) -> DatastoreInfo:
        return parse_datastore_info_from_xml(_info(self._function, self._id, xml=True))
    
    def update(self, template: str, append: bool = False) -> None:
        _update(self._function, self._id, template, append)

