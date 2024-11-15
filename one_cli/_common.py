import xml.etree.ElementTree as xmlTree
from dataclasses    import dataclass
from typing         import Optional


@dataclass
class Permissions:
    OWNER_U:  int
    OWNER_M:  int
    OWNER_A:  int

    GROUP_U:  int
    GROUP_M:  int
    GROUP_A:  int

    OTHER_U:  int
    OTHER_M:  int
    OTHER_A:  int


@dataclass
class LockStatus:
    LOCKED:     int
    OWNER:      int
    TIME:       int
    REQ_ID:     int



def parse_permissions_from_xml(raw_xml: str) -> Permissions:
    xml = xmlTree.fromstring(raw_xml)
    xml_permissions = xml.find('PERMISSIONS')

    return Permissions(
            OWNER_U= int(xml_permissions.find('OWNER_U').text),
            OWNER_M= int(xml_permissions.find('OWNER_M').text),
            OWNER_A= int(xml_permissions.find('OWNER_A').text),

            GROUP_U= int(xml_permissions.find('GROUP_U').text),
            GROUP_M= int(xml_permissions.find('GROUP_M').text),
            GROUP_A= int(xml_permissions.find('GROUP_A').text),

            OTHER_U= int(xml_permissions.find('OTHER_U').text),
            OTHER_M= int(xml_permissions.find('OTHER_M').text),
            OTHER_A= int(xml_permissions.find('OTHER_A').text),
        )


def parse_lock_from_xml(raw_xml: str) -> Optional[LockStatus]:
    xml  = xmlTree.fromstring(raw_xml)
    lock = None
    if xml.find('LOCK'):
        lock = LockStatus(
            LOCKED=     int(xml.find('LOCK/LOCKED').text),
            OWNER=      int(xml.find('LOCK/OWNER').text),
            TIME=       int(xml.find('LOCK/TIME').text),
            REQ_ID=     int(xml.find('LOCK/REQ_ID').text)
        )
    return lock