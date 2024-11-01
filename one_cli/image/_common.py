import xml.etree.ElementTree as xmlTree

from dataclasses        import dataclass, field
from typing             import List, Dict, Optional
from one_cli._common    import UnitPermissions, Permissions, LockStatus




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
class SnapshotInfo:
    ID:         int
    NAME:       str
    DATE:       int
    PARENT:     int
    ACTIVE:     bool
    CHILDREN:   List[int] = field(default_factory=list)




@dataclass
class ImageInfo:
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
    VMS:                List[int]            = field(default_factory=list)
    SNAPSHOTS:          List[SnapshotInfo]   = field(default_factory=list)
    TEMPLATE:           Dict[str, str]       = field(default_factory=dict)
    LOCK:               Optional[LockStatus] = None



def parse_image_info_from_xml(raw_image_xml: str) -> ImageInfo:
    image_xml = xmlTree.fromstring(raw_image_xml)

    snapshots = []
    snapshots_elements = image_xml.find('SNAPSHOTS')
    for snapshot in snapshots_elements.findall('SNAPSHOT'):
        snapshots.append(
            SnapshotInfo(
                ID=         int(snapshot.find('ID').text),
                NAME=       snapshot.find('NAME').text,
                DATE=       int(snapshot.find('DATE').text),
                PARENT=     int(snapshot.find('PARENT').text),
                ACTIVE=     snapshot.find('ACTIVE') == "Yes",
                CHILDREN=   [int(child) for child in snapshot.findtext('CHILDREN', '').split() if child.isdigit()],
        ))

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
    
    lock = None
    if image_xml.find('LOCK'):
        lock = LockStatus(
            LOCKED=     int(image_xml.find('LOCK/LOCKED').text),
            OWNER=      int(image_xml.find('LOCK/OWNER').text),
            TIME=       int(image_xml.find('LOCK/TIME').text),
            REQ_ID=     int(image_xml.find('LOCK/REQ_ID').text)
        )


    image_info = ImageInfo(
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
            TEMPLATE=           {attribulte.tag: attribulte.text or "" for attribulte in image_xml.find('TEMPLATE')},
            VMS=                [int(vm_id.text) for vm_id in image_xml.find('VMS').findall('ID')],
            SNAPSHOTS=          snapshots,
            LOCK=               lock,
        )
    
    return image_info



