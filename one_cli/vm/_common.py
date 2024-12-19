import xml.etree.ElementTree as xmlTree

from dataclasses        import dataclass, field
from typing             import List, Dict, Optional, Union
from one_cli._common    import Permissions, parse_lock_from_xml, parse_permissions_from_xml, LockStatus






def __parse_template(raw_template_xml):
    template = {}
    xml = xmlTree.fromstring(raw_template_xml)
    template_element = xml.find(f'TEMPLATE')
    
    for element in template_element:
        if len(element) == 0:
            template[element.tag] = element.text
        elif element.tag in template:
            template[element.tag].append({_.tag: _.text or "" for _ in element.iter() if _ is not element})
        else:
            template[element.tag] = [{_.tag: _.text or "" for _ in element.iter() if _ is not element}]
                
    return template





@dataclass
class VirtualMachineInfo:
    ID:                 int
    UID:                int
    GID:                int
    UNAME:              str
    GNAME:              str
    NAME:               str
    PERMISSIONS:        Permissions
    LOCK:               LockStatus
    LAST_POLL:          int
    STATE:              int
    LCM_STATE:          int
    PREV_STATE:         int
    PREV_LCM_STATE:     int
    RESCHED:            int
    STIME:              int
    ETIME:              int
    DEPLOY_ID:          str
    TEMPLATE:           Dict[str, List[Dict[str, str]]] = field(default_factory=dict)
    USER_TEMPLATE:      Dict[str, str]                  = field(default_factory=dict)
    





def parse_vm_info_from_xml(raw_vm_xml: str) -> VirtualMachineInfo:
    xml         = xmlTree.fromstring(raw_vm_xml)
    permissions = parse_permissions_from_xml(raw_vm_xml)
    template    = __parse_template(raw_vm_xml)
    lock        = parse_lock_from_xml(raw_vm_xml)


    vm_info = VirtualMachineInfo(
            ID=                 int(xml.find('ID').text),
            UID=                int(xml.find('UID').text),
            GID=                int(xml.find('GID').text),
            UNAME=              xml.find('UNAME').text,
            GNAME=              xml.find('GNAME').text,
            NAME=               xml.find('NAME').text,
            PERMISSIONS=        permissions,
            LAST_POLL=          int(xml.find('LAST_POLL').text),
            STATE=              int(xml.find('STATE').text),
            LCM_STATE=          int(xml.find('LCM_STATE').text),
            PREV_STATE=         int(xml.find('PREV_STATE').text),
            PREV_LCM_STATE=     int(xml.find('PREV_LCM_STATE').text),
            RESCHED=            int(xml.find('RESCHED').text),
            STIME=              int(xml.find('STIME').text),
            ETIME=              int(xml.find('ETIME').text),
            DEPLOY_ID=          xml.find('DEPLOY_ID').text,
            TEMPLATE=           template,
            USER_TEMPLATE=      {attribulte.tag: attribulte.text or "" for attribulte in xml.find('USER_TEMPLATE')},
            LOCK=               lock,
        )
    
    return vm_info



