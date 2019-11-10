from generation.test_case.generator import *
from generation.attack_tree.loader import *
from generation.attack_tree.translator import *

fdr_path = "/Applications/FDR4.app/Contents/Frameworks"
attack_tree_file = "data/Vehicle_Compromise.xml"

loader = AttackTreeLoader(attack_tree_file)
tree = loader.load()

translator = AttackTreeTranslator()
csp_file = translator.gen_csp_file(tree)

generator = Generator(fdr_path, csp_file)
tcs = generator.gen_all_test_cases()

for tc in tcs:
    output = " -> ".join(tc)
    print(output)
