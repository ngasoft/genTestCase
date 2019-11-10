class AttackTree(object):
    def __init__(self, label):
        self.label = label
        self.test_script = None
        self.children = list()
        self.source = None

    def add_child(self, sub):
        self.children.append(sub)

    def is_leaf(self):
        return not self.children


class AndNode(AttackTree):
    def __init__(self, label):
        super(AndNode, self).__init__(label)

class OrNode(AttackTree):
    def __init__(self, label):
        super(OrNode, self).__init__(label)


class SandNode(AttackTree):
    def __init__(self, label):
        super(SandNode, self).__init__(label)


