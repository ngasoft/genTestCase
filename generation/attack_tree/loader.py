import xml.etree.ElementTree as ET
#from enum import Enum, auto
import generation.attack_tree.attack_tree as at


class NodeType: #(Enum):
    OR_NODE = "disjunctive"
    AND_NODE = "conjunctive"
    SAND_NODE = "sequential"
    ROOT = "sandtree"
    NODE = "node"
    LABEL = "label"
    TESTING_SCRIPT = "comment"
    NOTE_TYPE = "refinement"


class AttackTreeLoader:
    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):
        tree = ET.parse(self.file_name)
        root = tree.getroot().find(NodeType.NODE)

        ret = self.parse_xml_node(root)

        return ret

    def parse_xml_node(self, node):
        label = node.find(NodeType.LABEL).text
        tree = None
        if node.get(NodeType.NOTE_TYPE) == NodeType.OR_NODE:
            tree = at.OrNode(label)
        elif node.get(NodeType.NOTE_TYPE) == NodeType.AND_NODE:
            tree = at.AndNode(label)
        elif node.get(NodeType.NOTE_TYPE) == NodeType.SAND_NODE:
            tree = at.SandNode(label)

        script = node.find(NodeType.TESTING_SCRIPT)
        if script is not None:
            tree.test_script = script.text

        for c in node.findall(NodeType.NODE):
            tree.add_child(self.parse_xml_node(c))

        tree.source = self.file_name
        return tree
