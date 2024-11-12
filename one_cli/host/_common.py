import xml.etree.ElementTree as xmlTree

from dataclasses        import dataclass, field
from typing             import List, Dict





@dataclass
class HostInfo:
    ID:                 int
    NAME:               str
    STATE:              int
    PREV_STATE:         int
    IM_MAD:             str
    VM_MAD:             str
    CLUSTER_ID:         int
    CLUSTER:            str
#   HOST_SHARE:
#   VMS:
#   MONITORING:
    TEMPLATE:           Dict[str, str]       = field(default_factory=dict)

    




def parse_host_info_from_xml(raw_host_xml: str) -> HostInfo:
    xml = xmlTree.fromstring(raw_host_xml)

    host_info = HostInfo(
            ID=                 int(xml.find('ID').text),
            NAME=               xml.find('NAME').text,
            STATE=              int(xml.find('STATE').text),
            PREV_STATE=         int(xml.find('PREV_STATE').text),
            CLUSTER_ID=         int(xml.find('CLUSTER_ID').text),
            CLUSTER=            xml.find('CLUSTER').text,
            IM_MAD=             xml.find('IM_MAD').text,
            VM_MAD=             xml.find('VM_MAD').text,
            TEMPLATE=           {attribulte.tag: attribulte.text or "" for attribulte in xml.find('TEMPLATE')},
            )

    return host_info


