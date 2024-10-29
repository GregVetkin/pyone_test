import xml.etree.ElementTree as xmlTree

from utils          import run_command
from dataclasses    import dataclass



@dataclass
class UnitPermissions:
    USE:    bool
    MANAGE: bool
    ADMIN:  bool


@dataclass
class Permissions:
    OWNER:  UnitPermissions
    GROUP:  UnitPermissions
    OTHER:  UnitPermissions


@dataclass
class ImageData:
    ID:                 int
    UID:                int
    GID:                int
    UNAME:              str
    GNAME:              str
    NAME:               str
    PERMISSIONS:        Permissions
    TYPE:               int
    DISK_TYPE:          int
    PERSISTENT:         bool
    REGTIME:            int
    SOURCE:             str
    PATH:               str
    FORMAT:             str
    FS:                 str
    SIZE:               int
    STATE:              int
    PREV_STATE:         int
    RUNNING_VMS:        int
    CLONING_OPS:        int
    CLONING_ID:         int
    TARGET_SNAPSHOT:    int
    DATASTORE_ID:       int
    DATASTORE:          str



class Image:
    def __init__(self, image_id: int) -> None:
        self._image_id = image_id


    def info(self) -> ImageData:
        raw_image_xml = run_command(f"sudo oneimage show {self._image_id} -x")
        image_xml     = xmlTree.fromstring(raw_image_xml)

        owner_permissions = UnitPermissions(
            USE=    bool(int(image_xml.find('PERMISSIONS/OWNER_U').text)),
            MANAGE= bool(int(image_xml.find('PERMISSIONS/OWNER_M').text)),
            ADMIN=  bool(int(image_xml.find('PERMISSIONS/OWNER_A').text)),
        )

        group_permissions = UnitPermissions(
            USE=    bool(int(image_xml.find('PERMISSIONS/GROUP_U').text)),
            MANAGE= bool(int(image_xml.find('PERMISSIONS/GROUP_M').text)),
            ADMIN=  bool(int(image_xml.find('PERMISSIONS/GROUP_A').text)),
        )

        other_permissions = UnitPermissions(
            USE=    bool(int(image_xml.find('PERMISSIONS/OTHER_U').text)),
            MANAGE= bool(int(image_xml.find('PERMISSIONS/OTHER_M').text)),
            ADMIN=  bool(int(image_xml.find('PERMISSIONS/OTHER_A').text)),
        )

        permissions = Permissions(
            OWNER=  owner_permissions,
            GROUP=  group_permissions,
            OTHER=  other_permissions,
        )

        image_info = ImageData(
            ID=                 int(image_xml.find('ID').text),
            UID=                int(image_xml.find('UID').text),
            GID=                int(image_xml.find('GID').text),
            UNAME=              image_xml.find('UNAME').text,
            GNAME=              image_xml.find('GNAME').text,
            NAME=               image_xml.find('NAME').text,
            PERMISSIONS=        permissions,
            TYPE=               int(image_xml.find('TYPE').text),
            DISK_TYPE=          int(image_xml.find('DISK_TYPE').text),
            PERSISTENT=         bool(int(image_xml.find('PERSISTENT').text)),
            REGTIME=            int(image_xml.find('REGTIME').text),
            SOURCE=             image_xml.find('SOURCE').text,
            PATH=               image_xml.find('PATH').text,
            FORMAT=             image_xml.find('FORMAT').text,
            FS=                 image_xml.find('FS').text,
            SIZE=               int(image_xml.find('SIZE').text),
            STATE=              int(image_xml.find('STATE').text),
            PREV_STATE=         int(image_xml.find('PREV_STATE').text),
            RUNNING_VMS=        int(image_xml.find('RUNNING_VMS').text),
            CLONING_OPS=        int(image_xml.find('CLONING_OPS').text),
            CLONING_ID=         int(image_xml.find('CLONING_ID').text),
            TARGET_SNAPSHOT=    int(image_xml.find('TARGET_SNAPSHOT').text),
            DATASTORE_ID=       int(image_xml.find('DATASTORE_ID').text),
            DATASTORE=          image_xml.find('DATASTORE').text,
        )
        return image_info
    

if __name__ == "__main__":
    img = Image(193)
    data = img.info()
    print(data)