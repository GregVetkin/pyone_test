from one_cli.datastore._common  import DatastoreInfo, parse_datastore_info_from_xml
from one_cli._base_commands     import _chmod, _chown, _delete, _info, _update, _exist, _create
from one_cli.image              import force_delete_image


FUNCTION_NAME = "onedatastore"


def datastore_exist(datastore_id: int) -> bool:
    return _exist(FUNCTION_NAME, datastore_id)


def create_datastore(datastore_template: str) -> int:
    return _create(FUNCTION_NAME, datastore_template)



def force_delete_datastore(datastore_id: int):
    if not datastore_exist(datastore_id):
        return

    datastore = Datastore(datastore_id)
    datastore_info = datastore.info()
    
    for image_id in datastore_info.IMAGES:
        force_delete_image(image_id)

    datastore.delete()




class Datastore:
    def __init__(self, datastore_id: int) -> None:
        self._id        = datastore_id
        self._function  = FUNCTION_NAME
    
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

