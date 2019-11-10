from generation.attack_tree.attack_tree import *
import os


class AttackTreeTranslator:
    def __init__(self):
        self.inc = 0
        self.script = list()
        self.used_names = set()
        self.used_events = dict()
        self.action_dict = dict()

    def get_events(self):
        return self.used_events.values()

    def translate(self, tree):
        if tree.is_leaf():
            event = self.gen_csp_event_name(tree.label)
            process = self.gen_csp_process_name(tree.label)
            self.script.append(process + " = " + event + " -> SKIP")
            if tree.test_script is not None:
                self.action_dict[event] = tree.test_script
            return process
        elif isinstance(tree, OrNode):
            sub_processes = list()
            for n in tree.children:
                sub_processes.append(self.translate(n))
            process = self.gen_csp_process_name(tree.label)
            self.script.append(process + " = " + " [] ".join(sub_processes))
            return process
        elif isinstance(tree, AndNode):
            sub_processes = list()
            for n in tree.children:
                sub_processes.append(self.translate(n))
            process = self.gen_csp_process_name(tree.label)
            self.script.append(process + " = " + " ||| ".join(sub_processes))
            return process
        elif isinstance(tree, SandNode):
            sub_processes = list()
            for n in tree.children:
                sub_processes.append(self.translate(n))
            process = self.gen_csp_process_name(tree.label)
            self.script.append(process + " = " + "; ".join(sub_processes))
            return process

    def gen_csp_file(self, tree):
        main_process = self.translate(tree)
        csp = ["channel " + e for e in self.get_events()]
        csp.extend(self.script)
        csp.append("Attacker = " + main_process)
        csp_script = "\n".join(csp)

        csp_file_name = tree.source.split(os.path.sep)[-1] + ".csp"
        f = open(csp_file_name, 'w')
        f.write(csp_script)
        f.close()

        return csp_file_name


    def gen_csp_name(self, label):
        char_array = list(label)
        l = len(label)
        for i in range(l):
            if not char_array[i].isdigit() and not char_array[i].isalpha():
                char_array[i] = '_'

        return ''.join(char_array)

    def gen_csp_event_name(self, label):
        if label not in self.used_events:
            event = "event_" + self.gen_csp_name(label)
            if event in self.used_events.values():
                n = self.used_events.values().size()
                n += 1
                event += "_" + str(n)
            self.used_events[label] = event

        return self.used_events[label]

    def gen_csp_process_name(self, label):
        name = "Process_" + self.gen_csp_name(label)
        if name in self.used_names:
            n = self.used_names.size()
            n += 1
            name = name + "_" + str(n)
        self.used_names.add(name)
        return name
