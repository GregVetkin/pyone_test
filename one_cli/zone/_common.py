import xml.etree.ElementTree as xmlTree

from dataclasses        import dataclass, field
from typing             import List, Dict





@dataclass
class ZoneInfo:
    ID:                 int
    NAME:               str
    TEMPLATE:           Dict[str, str] = field(default_factory=dict)
    #SERVER_POOL:        ---




def parse_zone_info_from_xml(raw_zone_xml: str) -> ZoneInfo:
    xml = xmlTree.fromstring(raw_zone_xml)

    zone_info = ZoneInfo(
                ID=                 int(xml.find('ID').text),
                NAME=               xml.find('NAME').text,
                TEMPLATE=           {attribulte.tag: attribulte.text or "" for attribulte in xml.find('TEMPLATE')},
                )

    return zone_info


