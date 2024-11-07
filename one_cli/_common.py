import xml.etree.ElementTree as xmlTree

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
class LockStatus:
    LOCKED:     int
    OWNER:      int
    TIME:       int
    REQ_ID:     int




def parse_permissions_from_xml(raw_xml: str) -> Permissions:
    xml = xmlTree.fromstring(raw_xml)

    owner_permissions = UnitPermissions(
            USE=    bool(int(xml.find('PERMISSIONS/OWNER_U').text)),
            MANAGE= bool(int(xml.find('PERMISSIONS/OWNER_M').text)),
            ADMIN=  bool(int(xml.find('PERMISSIONS/OWNER_A').text)),
        )

    group_permissions = UnitPermissions(
            USE=    bool(int(xml.find('PERMISSIONS/GROUP_U').text)),
            MANAGE= bool(int(xml.find('PERMISSIONS/GROUP_M').text)),
            ADMIN=  bool(int(xml.find('PERMISSIONS/GROUP_A').text)),
        )

    other_permissions = UnitPermissions(
            USE=    bool(int(xml.find('PERMISSIONS/OTHER_U').text)),
            MANAGE= bool(int(xml.find('PERMISSIONS/OTHER_M').text)),
            ADMIN=  bool(int(xml.find('PERMISSIONS/OTHER_A').text)),
        )


    return Permissions(
            OWNER=  owner_permissions,
            GROUP=  group_permissions,
            OTHER=  other_permissions,
        )