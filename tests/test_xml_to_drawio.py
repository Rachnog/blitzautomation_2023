import unittest

from xml.etree import ElementTree as ET
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
from src.drawio_utils import XMLToDrawIOConverter

class TestXMLConversion(unittest.TestCase):

    def test_number_of_nodes(self):
        input_xml = """
        <map>
            <node text="A">
                <node text="B">
                    <node text="D"></node>
                    <node text="E"></node>
                </node>
                <node text="C">
                    <node text="F"></node>
                </node>
            </node>
        </map>
        """

        converter = XMLToDrawIOConverter(input_xml)
        converted_xml = converter.convert()

        input_root = ET.fromstring(input_xml)
        input_nodes = input_root.findall(".//node")

        converted_root = ET.fromstring(converted_xml)
        converted_nodes = converted_root.findall(".//mxCell[@value]")

        self.assertEqual(len(input_nodes), len(converted_nodes))

    def test_number_of_edges(self):
        input_xml = """
        <map>
            <node text="A">
                <node text="B">
                    <node text="D"></node>
                    <node text="E"></node>
                </node>
                <node text="C">
                    <node text="F"></node>
                </node>
            </node>
        </map>
        """
        converter = XMLToDrawIOConverter(input_xml)
        converted_xml = converter.convert()

        input_root = ET.fromstring(input_xml)
        input_edges = input_root.findall(".//node/node")

        converted_root = ET.fromstring(converted_xml)
        converted_edges = converted_root.findall(".//mxCell[@edge='1']")

        self.assertEqual(len(input_edges), len(converted_edges))

    def test_edge_presence(self):
        input_xml = """
        <map>
            <node text="A">
                <node text="B">
                    <node text="D"></node>
                    <node text="E"></node>
                </node>
                <node text="C">
                    <node text="F"></node>
                </node>
            </node>
        </map>
        """
        converter = XMLToDrawIOConverter(input_xml)
        converted_xml = converter.convert()

        input_root = ET.fromstring(input_xml)
        node_a = input_root.find(".//node[@text='A']")
        node_b = node_a.find(".//node[@text='B']")

        converted_root = ET.fromstring(converted_xml)
        node_a_id = converted_root.find(".//mxCell[@value='A']").attrib['id']
        node_b_id = converted_root.find(".//mxCell[@value='B']").attrib['id']

        edge = converted_root.find(f".//mxCell[@source='{node_a_id}'][@target='{node_b_id}']")

        self.assertIsNotNone(edge)


if __name__ == '__main__':
    unittest.main()
