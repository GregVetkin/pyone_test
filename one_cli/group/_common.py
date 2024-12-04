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


def parse_vmquota(vm_quota_element: xmlTree.Element) -> Optional[VmQuotaInfo]:
    vmquota = vm_quota_element.find("VM")
    if vmquota is None: 
        return None
    
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



@dataclass
class NetworkQuotaInfo:
    ID:             int
    LEASES:         int
    LEASES_USED:    int

def parse_networkquota(network_quota_element: xmlTree.Element) -> List[NetworkQuotaInfo]:
    def _network_quota(xml_elem):
        return NetworkQuotaInfo(
            ID=             int(xml_elem.find("ID").text),
            LEASES=         int(xml_elem.find("LEASES").text),
            LEASES_USED=    int(xml_elem.find("LEASES_USED").text),
        )
    net_quota_list  = [_network_quota(net) for net in network_quota_element.findall("NETWORK")]
    return net_quota_list



@dataclass
class DatastoreQuotaInfo:
    ID:             int
    IMAGES:         int
    IMAGES_USED:    int
    SIZE:           int
    SIZE_USED:      int

def parse_datastorequota(datastore_quota_element: xmlTree.Element) -> List[DatastoreQuotaInfo]:
    def _datastore_quota(xml_elem):
        return DatastoreQuotaInfo(
            ID=             int(xml_elem.find("ID").text),
            IMAGES=         int(xml_elem.find("IMAGES").text),
            IMAGES_USED=    int(xml_elem.find("IMAGES_USED").text),
            SIZE=           int(xml_elem.find("SIZE").text),
            SIZE_USED=      int(xml_elem.find("SIZE_USED").text),
        )
    ds_quota_list  = [_datastore_quota(ds) for ds in datastore_quota_element.findall("DATASTORE")]
    return ds_quota_list



@dataclass
class ImageQuotaInfo:
    ID: int
    RVMS: int
    RVMS_USED: int

def parse_imagequota(image_quota_element: xmlTree.Element) -> List[ImageQuotaInfo]:
    def _image_quota(xml_elem):
        return ImageQuotaInfo(
            ID=           int(xml_elem.find("ID").text),
            RVMS=         int(xml_elem.find("RVMS").text),
            RVMS_USED=    int(xml_elem.find("RVMS_USED").text),
        )
    image_quota_list  = [_image_quota(image) for image in image_quota_element.findall("IMAGE")]
    return image_quota_list




@dataclass
class DefaultGroupQuotasInfo:
        DATASTORE_QUOTA:    Optional[List[DatastoreQuotaInfo]]  = field(default_factory=None)
        NETWORK_QUOTA:      Optional[List[NetworkQuotaInfo]]    = field(default_factory=None)
        VM_QUOTA:           Optional[VmQuotaInfo]               = field(default_factory=None)
        IMAGE_QUOTA:        Optional[List[ImageQuotaInfo]]      = field(default_factory=None)


def parse_default_group_quotas(default_group_quotas_element: xmlTree.Element) -> DefaultGroupQuotasInfo:
    return DefaultGroupQuotasInfo(
        DATASTORE_QUOTA=    parse_datastorequota(default_group_quotas_element.find("DATASTORE_QUOTA")),
        NETWORK_QUOTA=      parse_networkquota(default_group_quotas_element.find("NETWORK_QUOTA")),
        VM_QUOTA=           parse_vmquota(default_group_quotas_element.find("VM_QUOTA")),
        IMAGE_QUOTA=        parse_imagequota(default_group_quotas_element.find("IMAGE_QUOTA")),
    )



@dataclass
class GroupInfo:
    ID:                     int
    NAME:                   str
    TEMPLATE:               Dict[str, List[Dict[str, str]]]     = field(default_factory=dict)
    USERS:                  List[int]                           = field(default_factory=list)
    ADMINS:                 List[int]                           = field(default_factory=list)
    DATASTORE_QUOTA:        Optional[List[DatastoreQuotaInfo]]  = field(default_factory=None)
    NETWORK_QUOTA:          Optional[List[NetworkQuotaInfo]]    = field(default_factory=None)
    VM_QUOTA:               Optional[VmQuotaInfo]               = field(default_factory=None)
    IMAGE_QUOTA:            Optional[List[ImageQuotaInfo]]      = field(default_factory=None)
    DEFAULT_GROUP_QUOTAS:   Optional[DefaultGroupQuotasInfo]    = field(default_factory=None)





def __parse_template(template_element: xmlTree.Element):
    template = {}
    
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
    
    template        = __parse_template(xml.find("TEMPLATE"))
    datastore_quota = parse_datastorequota(xml.find("DATASTORE_QUOTA"))
    network_quota   = parse_networkquota(xml.find("NETWORK_QUOTA"))
    vm_quota        = parse_vmquota(xml.find("VM_QUOTA"))
    image_quota     = parse_imagequota(xml.find("IMAGE_QUOTA"))
    default_quotas  = parse_default_group_quotas(xml.find("DEFAULT_GROUP_QUOTAS"))

    return GroupInfo(
            ID=                     int(xml.find('ID').text),
            NAME=                   xml.find('NAME').text,
            TEMPLATE=               template,
            USERS=                  [int(vm_id.text) for vm_id in xml.find('USERS').findall('ID')],
            ADMINS=                 [int(vm_id.text) for vm_id in xml.find('ADMINS').findall('ID')],
            DATASTORE_QUOTA=        datastore_quota,
            NETWORK_QUOTA=          network_quota,
            VM_QUOTA=               vm_quota,
            IMAGE_QUOTA=            image_quota,
            DEFAULT_GROUP_QUOTAS=   default_quotas,
        )
