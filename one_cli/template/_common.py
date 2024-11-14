import xml.etree.ElementTree as xmlTree

from dataclasses        import dataclass, field
from typing             import List, Dict, Optional
from one_cli._common    import Permissions, parse_permissions_from_xml, Permissions, LockStatus, parse_lock_from_xml





@dataclass
class TemplateInfo:
    ID:                 int
    UID:                int
    GID:                int
    UNAME:              str
    GNAME:              str
    NAME:               str
    PERMISSIONS:        Permissions
    REGTIME:            int
    LOCK:               Optional[LockStatus] = None
    TEMPLATE:           Dict[str, str]       = field(default_factory=dict)




def parse_template_info_from_xml(raw_template_xml: str) -> TemplateInfo:
    xml = xmlTree.fromstring(raw_template_xml)
    permissions = parse_permissions_from_xml(raw_template_xml)
    lock = parse_lock_from_xml(raw_template_xml)

    
    template_info = TemplateInfo(
                ID=                 int(xml.find('ID').text),
                UID=                int(xml.find('UID').text),
                GID=                int(xml.find('GID').text),
                UNAME=              xml.find('UNAME').text,
                GNAME=              xml.find('GNAME').text,
                NAME=               xml.find('NAME').text,
                REGTIME=            int(xml.find('REGTIME').text),
                PERMISSIONS=        permissions,
                LOCK=               lock,
                TEMPLATE=           {attribulte.tag: attribulte.text or "" for attribulte in xml.find('TEMPLATE')},
                )

    return template_info


