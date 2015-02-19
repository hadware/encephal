import xml.etree.ElementTree as ET

def CDATA(text=None):
    element = ET.Element('![CDATA[')
    element.text = text
    return element

ET._original_serialize_xml = ET._serialize_xml
def _serialize_xml(write, elem, qnames, namespaces, short_empty_elements):
    if elem.tag == '![CDATA[':
        write("\n<%s%s]]>\n" % (
                elem.tag, elem.text))
        return
    return ET._original_serialize_xml(write, elem, qnames, namespaces, short_empty_elements)
ET._serialize_xml = ET._serialize['xml'] = _serialize_xml


if __name__ == "__main__":
    import sys

    text = """
    <?xml version='1.0' encoding='utf-8'?>
    <text>
    This is just some sample text.
    </text>
    """

    root = ET.Element("data")
    style = ET.SubElement(root, "style", type="text/css")
    cdata = ET.SubElement(style, '![CDATA[')
    cdata.text = "rect { stroke: #000000;}"
    et = ET.ElementTree(root)
    et.write("test.svg", "utf-8")
