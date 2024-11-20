import xml.etree.ElementTree as xmlTree

from dataclasses        import dataclass, field
from typing             import List, Dict, Union, Optional
from one_cli._common    import Permissions, parse_permissions_from_xml, Permissions, LockStatus, parse_lock_from_xml


def __convert(text: str) -> Union[str, int, float]:
    try:
        return int(text)
    except Exception:
        pass
    
    try:
        return float(text)
    except Exception:
        pass

    return text


def __parse_template(raw_template_xml):
    template = {}
    xml = xmlTree.fromstring(raw_template_xml)
    template_element = xml.find(f'TEMPLATE')
    
    for element in template_element:
        if len(element) == 0:
            template[element.tag] = __convert(element.text)
        else:
            if element.tag in template:
                template[element.tag].append({_.tag: __convert(_.text) or "" for _ in element.iter() if _ is not element})
            else:
                template[element.tag] = [{_.tag: __convert(_.text) or "" for _ in element.iter() if _ is not element}]
                
    return template





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
    TEMPLATE:           Dict[str, List[Dict[str, str]]] = field(default_factory=dict)




def parse_template_info_from_xml(raw_template_xml: str) -> TemplateInfo:
    xml         = xmlTree.fromstring(raw_template_xml)
    permissions = parse_permissions_from_xml(raw_template_xml)
    lock        = parse_lock_from_xml(raw_template_xml)
    template    = __parse_template(raw_template_xml)
    
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
                TEMPLATE=           template,
                )

    return template_info


