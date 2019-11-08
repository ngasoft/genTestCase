from generation.attack_tree.attack_tree import *


class AttackTreeTranslator:
    def __init__(self):
        self.inc = 0
        self.channels = set()
        self.script = list()

    def translate(self, tree):
        if tree.is_empty():
            event = "action_" + self.gen_csp_name(tree.label)
            process = ""
            self.channels.add(event)
            self.script.append(process + " = " + event + " -> SKIP")
            return process
        elif isinstance(tree, OrNode):
            sub_processes = list()
            for n in tree.children:
                sub_processes.append(self.translate(n))
            process = ""
            self.script.append(process + " = " + " [] ".join(sub_processes))
            return process
        elif isinstance(tree, AndNode):
            sub_processes = list()
            for n in tree.children:
                sub_processes.append(self.translate(n))
            process = ""
            self.script.append(process + " = " + " ||| ".join(sub_processes))
            return process
        elif isinstance(tree, SandNode):
            sub_processes = list()
            for n in tree.children:
                sub_processes.append(self.translate(n))
            process = ""
            self.script.append(process + " = " + "; ".join(sub_processes))

