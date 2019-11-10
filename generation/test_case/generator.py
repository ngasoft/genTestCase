from generation.test_case.templates import CSPTemplate
from string import Template
import sys

class Generator:
    def __init__(self, path_to_fdr, csp_file_name):
        global fdr_module
        sys.path.append(path_to_fdr)
        self.fdr_module = __import__('fdr')
        self.fdr_module.library_init()

        self.csp_file_name = csp_file_name
        base_name = csp_file_name[:-4]
        self.attack_tree_csp_file_name = csp_file_name
        self.test_cases_csp_file_name = base_name + "_test_cases.csp"
        self.test_cases_py_file_name = base_name + "_test_cases.py"
        self.main_csp_file_name = base_name + "_main.csp"

    def init_main_csp(self):
        csp_template = Template(CSPTemplate.main_csp)
        csp_script = csp_template.substitute(attack_tree_csp=self.attack_tree_csp_file_name, test_cases_csp=self.test_cases_csp_file_name)

        f = open(self.main_csp_file_name, 'w')
        f.write(csp_script)
        f.close()

    def gen_test_case_python_script(self, counter_examples, action_dict):
        script = "TC_COUNT = " + str(len(counter_examples)) + "\n"
        n = 1
        for attack in counter_examples:
            action_list = ["(\"" + action + "\"," + ("\"" + action_dict[action] + "\"" if action in action_dict else "None") + ")" for action in attack[:-1]]
            script += "TC_" + str(n) + " = [" + ", ".join(action_list) + " ] \n"
            n += 1
        test_cases = ["TC_" + str(i + 1) for i in range(n - 1)]
        script += "Test_Cases = [" + ", ".join(test_cases) + "]"

        f = open(self.test_cases_py_file_name, 'w')
        f.write(script)
        f.close()
        return self.test_cases_py_file_name

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

    def call_fdr(self):
        session = self.fdr_module.Session()

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