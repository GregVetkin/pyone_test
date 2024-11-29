import xml.etree.ElementTree as xmlTree

from dataclasses        import dataclass, field
from typing             import List, Dict, Optional



@dataclass
class VmQuotaInfo:
    CPU:                    int
    CPU_USED:               int
    MEMORY:                 int
    MEMORY_USED:            int
    RUNNING_CPU:            int
    RUNNING_CPU_USED:       int
    RUNNING_MEMORY:         int
    RUNNING_MEMORY_USED:    int
    RUNNING_VMS:            int
    RUNNING_VMS_USED:       int
    SYSTEM_DISK_SIZE:       int
    SYSTEM_DISK_SIZE_USED:  int
    VMS:                    int
    VMS_USED:               int


def parse_vmquota(raw_xml) -> Optional[VmQuotaInfo]:
    vmquota = xmlTree.fromstring(raw_xml).find("VM_QUOTA").find("VM")
    if vmquota:
        return VmQuotaInfo(
            CPU=                    int(vmquota.find('CPU').text),
            CPU_USED=               int(vmquota.find('CPU_USED').text),
            MEMORY=                 int(vmquota.find('MEMORY').text),
            MEMORY_USED=            int(vmquota.find('MEMORY_USED').text),
            RUNNING_CPU=            int(vmquota.find('RUNNING_CPU').text),
            RUNNING_CPU_USED=       int(vmquota.find('RUNNING_CPU_USED').text),
            RUNNING_MEMORY=         int(vmquota.find('RUNNING_MEMORY').text),
            RUNNING_MEMORY_USED=    int(vmquota.find('RUNNING_MEMORY_USED').text),
            RUNNING_VMS=            int(vmquota.find('RUNNING_VMS').text),
            RUNNING_VMS_USED=       int(vmquota.find('RUNNING_VMS_USED').text),
            SYSTEM_DISK_SIZE=       int(vmquota.find('SYSTEM_DISK_SIZE').text),
            SYSTEM_DISK_SIZE_USED=  int(vmquota.find('SYSTEM_DISK_SIZE_USED').text),
            VMS=                    int(vmquota.find('VMS').text),
            VMS_USED=               int(vmquota.find('VMS_USED').text),
        )
    else:
        return None


@dataclass
class NetworkQuotaInfo:
    ID:             int
    LEASES:         int
    LEASES_USED:    int

def parse_networkquota(raw_xml) -> Optional[List[NetworkQuotaInfo]]:
    def _network_quota(xml_elem):
        return NetworkQuotaInfo(
            ID=             int(xml_elem.find("ID").text),
            LEASES=         int(xml_elem.find("LEASES").text),
            LEASES_USED=    int(xml_elem.find("LEASES_USED").text),
        )
    netquota        = xmlTree.fromstring(raw_xml).find("NETWORK_QUOTA")
    net_quota_list  = [_network_quota(net) for net in netquota.findall("NETWORK")]
    return net_quota_list if net_quota_list else None



@dataclass
class DatastoreQuotaInfo:
    ID:             int
    IMAGES:         int
    IMAGES_USED:    int
    SIZE:           int
    SIZE_USED:      int

def parse_datastorequota(raw_xml) -> Optional[List[DatastoreQuotaInfo]]:
    def _datastore_quota(xml_elem):
        return DatastoreQuotaInfo(
            ID=             int(xml_elem.find("ID").text),
            IMAGES=         int(xml_elem.find("IMAGES").text),
            IMAGES_USED=    int(xml_elem.find("IMAGES_USED").text),
            SIZE=           int(xml_elem.find("SIZE").text),
            SIZE_USED=      int(xml_elem.find("SIZE_USED").text),
        )
    dsquota        = xmlTree.fromstring(raw_xml).find("DATASTORE_QUOTA")
    ds_quota_list  = [_datastore_quota(ds) for ds in dsquota.findall("DATASTORE")]
    return ds_quota_list if ds_quota_list else None




@dataclass
class ImageQuotaInfo:
    ID: int
    RVMS: int
    RVMS_USED: int

def parse_imagequota(raw_xml) -> Optional[List[ImageQuotaInfo]]:
    def _image_quota(xml_elem):
        return ImageQuotaInfo(
            ID=           int(xml_elem.find("ID").text),
            RVMS=         int(xml_elem.find("RVMS").text),
            RVMS_USED=    int(xml_elem.find("RVMS_USED").text),
        )
    imagequota        = xmlTree.fromstring(raw_xml).find("IMAGE_QUOTA")
    image_quota_list  = [_image_quota(image) for image in imagequota.findall("IMAGE")]
    return image_quota_list if image_quota_list else None





@dataclass
class GroupInfo:
    ID:                 int
    NAME:               str
    TEMPLATE:           Dict[str, List[Dict[str, str]]]     = field(default_factory=dict)
    USERS:              List[int]                           = field(default_factory=list)
    ADMINS:             List[int]                           = field(default_factory=list)
    DATASTORE_QUOTA:    Optional[List[DatastoreQuotaInfo]]  = field(default_factory=None)
    NETWORK_QUOTA:      Optional[List[NetworkQuotaInfo]]    = field(default_factory=None)
    VM_QUOTA:           Optional[VmQuotaInfo]               = field(default_factory=None)
    IMAGE_QUOTA:        Optional[List[ImageQuotaInfo]]      = field(default_factory=None)
    #DEFAULT_GROUP_QUOTAS:





def __parse_template(raw_template_xml):
    template = {}
    xml = xmlTree.fromstring(raw_template_xml)
    template_element = xml.find("TEMPLATE")
    
    for element in template_element:
        if len(element) == 0:
            template[element.tag] = element.text
        elif element.tag in template:
            template[element.tag].append({_.tag: _.text or "" for _ in element.iter() if _ is not element})
        else:
            template[element.tag] = [{_.tag: _.text or "" for _ in element.iter() if _ is not element}]
                
    return template



def parse_group_info_from_xml(raw_xml: str) -> GroupInfo:
    xml      = xmlTree.fromstring(raw_xml)
    
    template        = __parse_template(raw_xml)
    datastore_quota = parse_datastorequota(raw_xml)
    network_quota   = parse_networkquota(raw_xml)
    vm_quota        = parse_vmquota(raw_xml)
    image_quota     = parse_imagequota(raw_xml)

    return GroupInfo(
            ID=                 int(xml.find('ID').text),
            NAME=               xml.find('NAME').text,
            TEMPLATE=           template,
            USERS=              [int(vm_id.text) for vm_id in xml.find('USERS').findall('ID')],
            ADMINS=             [int(vm_id.text) for vm_id in xml.find('ADMINS').findall('ID')],
            DATASTORE_QUOTA=    datastore_quota,
            NETWORK_QUOTA=      network_quota,
            VM_QUOTA=           vm_quota,
            IMAGE_QUOTA=        image_quota,
        )
