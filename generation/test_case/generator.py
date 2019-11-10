import sys
from generation.test_case.templates import CSPTemplate
from string import Template

sys.path.append("/Applications/FDR4.app/Contents/Frameworks")
import fdr
fdr.library_init()


class Generator:
    def __init__(self, path_to_fdr, csp_file_name):
        self.path_to_fdr = path_to_fdr
        self.csp_file_name = csp_file_name
        base_name = csp_file_name
        self.attack_tree_csp_file_name = base_name
        self.test_cases_csp_file_name = base_name + ".test_cases.csp"
        self.main_csp_file_name = base_name + ".main.csp"

    def init_main_csp(self):
        csp_template = Template(CSPTemplate.main_csp)
        csp_script = csp_template.substitute(attack_tree_csp=self.attack_tree_csp_file_name, test_cases_csp=self.test_cases_csp_file_name)

        f = open(self.main_csp_file_name, 'w')
        f.write(csp_script)
        f.close()

    def generate_test_case(self):
        # call FDR
        counter_example = self.call_fdr()

        # if there is a counter example return by FDR, translate it into CSP and return, otherwise, return None
        if not (counter_example is None):
            return counter_example

        return None

    def gen_all_test_cases(self):
        counter_examples = []
        self.gen_test_cases_csp(counter_examples)
        self.init_main_csp()
        while True:
            tc = self.generate_test_case()
            if tc is not None:
                counter_examples.append(tc)
                self.gen_test_cases_csp(counter_examples)
            else:
                break
        return counter_examples

    def gen_test_cases_csp(self, counter_examples):
        csp_file = open(self.test_cases_csp_file_name, 'w')
        script = "Test_Cases = STOP\n"
        if counter_examples:
            script = self.counter_examples_to_csp(counter_examples)
        csp_file.write(script)
        csp_file.close()

    def counter_examples_to_csp(self, counter_examples):
        script = list()
        script.append("TC_COUNT = " + str(len(counter_examples)))

        n = 1
        for ce in counter_examples:
            script.append("TC(" + str(n) + ") = " + " -> ".join(ce) + " -> STOP")
            n += 1
        script.append("Test_Cases = [] i : {1.." + str(len(counter_examples)) + "} @ TC(i)")
        return "\n".join(script)

    def gen_test_cases_py_script(self, counter_examples):
        script = self.counter_examples_to_py(counter_examples)
        py_file = open('test_cases.py', 'w')
        py_file.write(script)
        py_file.close()


    def counter_examples_to_py(self, counter_examples):
        script = "TC_COUNT = " + str(len(counter_examples)) + "\n"
        n = 1
        for ce in counter_examples:
            ce_str = ['"' + e + '"' for e in ce[:-1]]
            script += "TC_" + str(n) + " = [" + ", ".join(ce_str) + " ] \n"
            n += 1
        TCs = ["TC_" + str(i + 1) for i in range(n - 1)]
        script += "Test_Cases = [" + ", ".join(TCs) + "]"
        return script

    def call_fdr(self):
        sys.path.append(self.path_to_fdr)
        session = fdr.Session()

        try:
            session.load_file(self.main_csp_file_name)
        except:
            print("Cannot load csp file")
            return 1

        assertion = session.assertions()[0]
        assertion.execute(None)
        if assertion.passed():
            print
            "Assertion passed, no more assertion is found"
            return None
        else:
            print
            "Found a counter examples:"
            ce = self.compile_counter_example(session, assertion)
            print
            "  " + " -> ".join(ce)
            return ce

    def compile_counter_example(self, session, assertion):
        ce = assertion.counterexamples()[0]
        trace = ce.implementation_behaviour().trace()
        event = ce.error_event()
        ce_trace = list(trace) + [event]
        return [session.uncompile_event(e).to_string() for e in ce_trace if e>1]