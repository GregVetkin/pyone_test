import xml.etree.ElementTree as xmlTree

from dataclasses        import dataclass, field
from typing             import List, Dict





@dataclass
class ClusterInfo:
    ID:            int
    NAME:          str
    HOSTS:         List[int] = field(default_factory=list)
    DATASTORES:    List[int] = field(default_factory=list)
    VNETS:         List[int] = field(default_factory=list)
    TEMPLATE:      Dict[str, str] = field(default_factory=dict)

    




def parse_cluster_info_from_xml(raw_host_xml: str) -> ClusterInfo:
    xml = xmlTree.fromstring(raw_host_xml)

    cluster_info = ClusterInfo(
            ID=           int(xml.find('ID').text),
            NAME=         xml.find('NAME').text,
            HOSTS=        [int(vm_id.text) for vm_id in xml.find('HOSTS').findall('ID')],
            DATASTORES=   [int(vm_id.text) for vm_id in xml.find('DATASTORES').findall('ID')],
            VNETS=        [int(vm_id.text) for vm_id in xml.find('VNETS').findall('ID')],
            TEMPLATE=     {attribulte.tag: attribulte.text or "" for attribulte in xml.find('TEMPLATE')},
            )

    return cluster_info
