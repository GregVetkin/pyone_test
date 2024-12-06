import xml.etree.ElementTree as xmlTree

from dataclasses    import make_dataclass
from utils          import run_command


def __correct_type(data: str):
    try:
        value = float(data)

        if value.is_integer():
            return int(value)
        
        return value
    
    except Exception:
        return data



def create_dataclass_from_xml(element: xmlTree.Element):
    fields = []
    values = {}

    for child in element:
        tag_name = child.tag.upper()
        fields.append(tag_name)

        if len(child) == 0:
            values[tag_name] = __correct_type(child.text)

        elif tag_name in values:
            if not isinstance(values[tag_name], list):
                values[tag_name] = [values[tag_name]]
            values[tag_name].append(create_dataclass_from_xml(child))

        else:
            values[tag_name] = create_dataclass_from_xml(child)

    fields = set(fields)
    DynamicClass = make_dataclass("DynamicDataClass", fields)
    return DynamicClass(**values)




vm_data_xml = run_command("ssh u@bufn1 'sudo oneimage show 52 -x'")
vm_data     = create_dataclass_from_xml(xmlTree.fromstring(vm_data_xml))

print(vm_data.TEMPLATE.FL)
print(type(vm_data.TEMPLATE.FL))