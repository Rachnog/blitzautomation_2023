# needed imports
import xml.etree.ElementTree as ET

class XMLQualityCheck:
    """
        Class for XML quality checks, check if the xml file is valid, has a minimum depth and width
        Input is a file path to the XML file
    """
    
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        
    def check_xml(self):
        """
            Check if the xml file is valid
        """
        try:
            ET.parse(self.xml_file)
            return True
        except ET.ParseError:
            return False
        
    def get_the_depth(self):
        """
            Get the depth of the xml file as the deepest level of the xml tree
        """
        return self._get_depth(self.root)
    
    def _get_depth(self, node):
        """
            Recursive function to get the depth of the xml file
        """
        if len(node) == 0:
            return 1
        else:
            return 1 + max(self._get_depth(child) for child in node)
        
    def get_the_width(self):
        """
            Get the width of the xml file as the maximum number of children of a node
        """
        return self._get_width(self.root)
    
    def _get_width(self, node):
        """
            Recursive function to get the width of the xml file
        """
        if len(node) == 0:
            return 1
        else:
            return max(len(node), max(self._get_width(child) for child in node))