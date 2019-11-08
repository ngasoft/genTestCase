class AttackTree:
    def __init__(self, label):
        self.label = label
        self.children = list()

    def add_child(self, sub):
        self.children.append(sub)

    def is_leaf(self):
        return not self.children


class AndNode(AttackTree):
    def __init__(self, label):
        super.__init__(label)

class OrNode(AttackTree):
    def __init__(self, label):
        super.__init__(label)


class SandNode(AttackTree):
    def __init__(self, label):
        super.__init__(label)


