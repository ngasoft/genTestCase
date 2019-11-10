from generation.test_case.generator import *
from generation.attack_tree.loader import *
from generation.attack_tree.translator import *

attack_tree_file = "data/Vehicle_Compromise.xml"

loader = AttackTreeLoader(attack_tree_file)
tree = loader.load()

translator = AttackTreeTranslator()
csp_file = translator.gen_csp_file(tree)

generator = Generator(fdr_path, csp_file)
tcs = generator.gen_all_test_cases()

generator.gen_test_case_python_script(tcs,translator.action_dict)