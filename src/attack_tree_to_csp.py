from treelib import Tree, Node
import re

def tree_to_csp(tree):
    csp_script = ""
    csp_channels = set()
    for node in tree.expand_tree(mode=Tree.DEPTH, key=lambda y: y.tag, reverse=False):
        csp_name = gen_csp_name(tree.get_node(node).tag)
        csp_body,channels = gen_csp_body(tree, node)
        csp_channels = csp_channels.union(channels)
        if node == tree.root:
            csp_script += "Attacker = " + csp_name + "\n"
        csp_script += csp_name + " = " + csp_body + "\n"

    channel_script = ""
    if len(csp_channels)>0:
        channel_script = "channel " + "\nchannel ".join(csp_channels)
    return channel_script + "\n" + csp_script;


def get_node_type(tree, node):
    children = tree.children(tree.get_node(node).identifier)
    if not children:
        return "LEAF"
    return children[0].tag.split(":")[0]


def gen_csp_name(s):
    name = s.split(":")[1]
    name = re.sub("[^a-zA-Z0-9]", "_", name)
    if '0' <= name[0] and name[0] <= '9':
        name = name[2:]
    else:
        name = name[1:]
    return name


def gen_csp_body(tree, node):
    type = get_node_type(tree, node)
    channels = set()
    if type == "LEAF":
        event = "action_" + gen_csp_name(tree.get_node(node).tag)
        channels.add(event)
        return event + " -> SKIP", channels
    if type == "SAND":
        sub_csp_names = [gen_csp_name(c.tag) for c in tree.children(node)]
        return " ; ".join(sub_csp_names), channels
    if type == "AND":
        sub_csp_names = [gen_csp_name(c.tag) for c in tree.children(node)]
        return " ||| ".join(sub_csp_names), channels
    if type == "OR":
        sub_csp_names = [gen_csp_name(c.tag) for c in tree.children(node)]
        return " [] ".join(sub_csp_names), channels
    return "UNRECOGNISED_OPERATOR", channels

