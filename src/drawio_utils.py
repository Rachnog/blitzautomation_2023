import xml.etree.ElementTree as ET

class XMLToDrawIOConverter:
    def __init__(self, xml_input):
        self.root = ET.fromstring(xml_input)
        self.cell_id = 2
        self.edge_id = 1000

    def generate_drawio_content(self, node, x, y, parent_id):
        content = []

        cell_value = node.get('text')
        cell_id = self.cell_id
        self.cell_id += 1

        content.append(f'<mxCell id="{cell_id}" value="{cell_value}" style="rounded=0;whiteSpace=wrap;html=1;" parent="1" vertex="1">')
        content.append(f'    <mxGeometry x="{x}" y="{y}" width="120" height="60" as="geometry"/>')
        content.append('</mxCell>')

        if parent_id is not None:
            edge_id = self.edge_id
            self.edge_id += 1

            content.append(f'<mxCell id="{edge_id}" style="edgeStyle=none;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;" parent="1" source="{parent_id}" target="{cell_id}" edge="1">')
            content.append('    <mxGeometry relative="1" as="geometry"/>')
            content.append('</mxCell>')

        y_child = y + 120
        x_child = x - 180 * (len(node.findall('node')) - 1) / 2
        for child_node in node.findall('node'):
            child_content, new_x_child = self.generate_drawio_content(child_node, x_child, y_child, cell_id)
            content.extend(child_content)
            x_child = new_x_child + 180

        return content, x_child

    def convert(self):
        content, _ = self.generate_drawio_content(self.root.find('node'), 260, 330, None)

        drawio_xml = f"""<mxfile host="65bd71144e">
    <diagram id="XT8NQRt45QgwYS0zmuNB" name="Page-1">
        <mxGraphModel dx="620" dy="482" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>
                {"".join(content)}
            </root>
        </mxGraphModel>
    </diagram>
</mxfile>"""

        return drawio_xml