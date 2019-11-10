import sys

fdr_path = None # this is the path to the file fdr.py in the installation of FDR
# for MacOS uncomment the following line
fdr_path = "/Applications/FDR4.app/Contents/Frameworks"
# for linux uncomment the following line
#fdr_path = path_to_fdr_folder + "/lib"

from generation.test_case.generator import *
from generation.attack_tree.loader import *
from generation.attack_tree.translator import *
from generation.test_case.executor import *

attack_tree_file = "data/Vehicle_Compromise.xml"

loader = AttackTreeLoader(attack_tree_file)
tree = loader.load()

translator = AttackTreeTranslator()
csp_file = translator.gen_csp_file(tree)

generator = Generator(fdr_path, csp_file)
tcs = generator.gen_all_test_cases()

test_cases_py = generator.gen_test_case_python_script(tcs,translator.action_dict)

executor = Executor(test_cases_py[:-3],None)

executor.execute()
