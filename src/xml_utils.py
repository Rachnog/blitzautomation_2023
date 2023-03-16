from lxml import etree

def save_xml_string_to_file(xml_string, output_file):
    """
        Save the xml string to a file
    """
    parser = etree.XMLParser(remove_blank_text=True)
    xml_element = etree.fromstring(xml_string, parser)
    tree = etree.ElementTree(xml_element)
    tree.write(output_file, pretty_print=True, encoding='utf-8', xml_declaration=True)