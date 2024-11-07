import xml.etree.ElementTree as xmlTree

from dataclasses        import dataclass, field
from typing             import List, Dict
from one_cli._common    import Permissions, parse_permissions_from_xml





@dataclass
class DatastoreInfo:
    ID:                 int
    UID:                int
    GID:                int
    UNAME:              str
    GNAME:              str
    NAME:               str
    PERMISSIONS:        Permissions
    DS_MAD:             str
    TM_MAD:             str
    BASE_PATH:          str
    TYPE:               int
    DISK_TYPE:          int
    STATE:              int
    TOTAL_MB:           int
    FREE_MB:            int
    USED_MB:            int
    CLUSTERS:           List[int]            = field(default_factory=list)
    IMAGES:             List[int]            = field(default_factory=list)
    TEMPLATE:           Dict[str, str]       = field(default_factory=dict)




def parse_datastore_info_from_xml(raw_datastore_xml: str) -> DatastoreInfo:
    xml = xmlTree.fromstring(raw_datastore_xml)
    permissions = parse_permissions_from_xml(raw_datastore_xml)
    
    datastore_info = DatastoreInfo(
                ID=                 int(xml.find('ID').text),
                UID=                int(xml.find('UID').text),
                GID=                int(xml.find('GID').text),
                UNAME=              xml.find('UNAME').text,
                GNAME=              xml.find('GNAME').text,
                NAME=               xml.find('NAME').text,
                PERMISSIONS=        permissions,
                DS_MAD=             xml.find('DS_MAD').text,
                TM_MAD=             xml.find('TM_MAD').text,
                BASE_PATH=          xml.find('BASE_PATH').text,
                TYPE=               int(xml.find('TYPE').text),
                DISK_TYPE=          int(xml.find('DISK_TYPE').text),
                STATE=              int(xml.find('STATE').text),
                TOTAL_MB=           int(xml.find('TOTAL_MB').text),
                FREE_MB=            int(xml.find('FREE_MB').text),
                USED_MB=            int(xml.find('USED_MB').text),
                CLUSTERS=           [int(cluster_id.text) for cluster_id in xml.find('CLUSTERS').findall('ID')],
                IMAGES=             [int(image_id.text) for image_id in xml.find('IMAGES').findall('ID')],
                TEMPLATE=           {attribulte.tag: attribulte.text or "" for attribulte in xml.find('TEMPLATE')},
                )

    return datastore_info


