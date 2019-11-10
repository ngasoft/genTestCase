from attack_tree_to_csp import tree_to_csp
from input_AT import create_attack_tree
import sys

# FDR_FOLDER = "/Applications/FDR3.app/Contents/Frameworks" # on macosx
FDR_FOLDER = "/usr/local/fdr/lib" # on linux
sys.path.append(FDR_FOLDER)
import fdr
fdr.library_init()

def gen_attack_csp_script():
    tree = create_attack_tree()
    csp_script = tree_to_csp(tree)
    csp_file = open('attack_tree.csp', 'w')
    csp_file.write(csp_script)
    csp_file.close()

    return True

gen_attack_csp_script()

def gen_a_test_case():

    # call FDR
    counter_example = call_FDR()

    # if there is a counter example return by FDR, translate it into CSP and return, otherwise, return None
    if not (counter_example is None):
        return counter_example

    return None

def gen_all_test_cases():
    counter_examples = []
    while True:
        tc = gen_a_test_case()
        if tc is not None:
            counter_examples.append(tc)
            gen_test_cases_csp_script(counter_examples)
        else:
            break
    gen_test_cases_py_script(counter_examples)
    return counter_examples

def gen_test_cases_csp_script(counter_examples):
    script = counter_examples_to_csp(counter_examples)
    csp_file = open('test_cases.csp', 'w')
    csp_file.write(script)
    csp_file.close()

def gen_test_cases_py_script(counter_examples):
    script = counter_examples_to_py(counter_examples)
    py_file = open('test_cases.py', 'w')
    py_file.write(script)
    py_file.close()

def counter_examples_to_csp(counter_examples):
    script = "TC_COUNT = " + str(len(counter_examples)) + "\n"
    n = 1
    for ce in counter_examples:
        script += "TC(" + str(n) + ") = " + " -> ".join(ce) + " -> STOP \n"
        n += 1
    script += "Test_Cases = [] i : {1.." + str(len(counter_examples)) + "} @ TC(i)"
    return script

def counter_examples_to_py(counter_examples):
    script = "TC_COUNT = " + str(len(counter_examples)) + "\n"
    n = 1
    for ce in counter_examples:
        ce_str = ['"' + e + '"' for e in ce[:-1]]
        script += "TC_" + str(n) + " = [" + ", ".join(ce_str) + " ] \n"
        n += 1
    TCs = ["TC_" + str(i+1) for i in range(n-1)]
    script += "Test_Cases = [" + ", ".join(TCs) + "]"
    return script

def init_test_cases_script():
    csp_file = open('test_cases.csp', 'w')
    csp_file.write("Test_Cases = STOP \n")
    csp_file.close()


def call_FDR():
    sys.path.append(FDR_FOLDER)
    session = fdr.Session()

    try:
        session.load_file("gen_test_cases.csp")
    except Exception, e:
        print "Cannot load csp file"
        return 1

    assertion = session.assertions()[0]
    assertion.execute(None)
    if assertion.passed():
        print "Assertion passed, no more assertion is found"
        return None
    else:
        print "Found a counter examples:"
        ce = compile_counter_example(session, assertion)
        print "  "  + " -> ".join(ce)
        return ce

def compile_counter_example(session, assertion):
    ce = assertion.counterexamples()[0]
    trace = ce.implementation_behaviour().trace()
    event = ce.error_event()
    ce_trace = list(trace) + [event]
    return [session.uncompile_event(e).to_string() for e in ce_trace if e>1]

#init_test_cases_script()
#gen_all_test_cases()
