from generation.attack_tree.translator import *
from generation.attack_tree.loader import *

attack_tree_file = "data/Vehicle_Compromise.xml"

loader = AttackTreeLoader(attack_tree_file)

tree = loader.load()
translator = AttackTreeTranslator()
translator.translate(tree)
csp = "\n".join(translator.script)
for e in translator.get_events():
    print("channel " + e)
print(csp)
