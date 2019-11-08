import xml.etree.ElementTree as ET
#from enum import Enum, auto
import generation.attack_tree as at


class NodeType: #(Enum):
    OR_NODE = "disjunctive"
    AND_NODE = "conjunctive"
    SAND_NODE = "sequential"


class AttackTreeLoader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.attachment = dict()

    def load(self):
        tree = ET.parse(self.file_name)
        root = list(tree.getroot())[0]

        self.parseXmlNode(root)

        return self.attachment[root]

    def parseXmlNode(self, node):
        children = list(node)
        label = children[0].text;

        if node.get("refinement") == NodeType.OR_NODE:
            tree = at.OrNode(label)
        elif node.get("refinement") == NodeType.AND_NODE:
            tree = at.AndNode(label)
        elif node.get("refinement") == NodeType.SAND_NODE:
            tree = at.SandNode(label)

        for c in children[1:]:
            tree.add_child(self.parseXmlNode(c))

        return tree
