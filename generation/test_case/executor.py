class Executor:
    def __init__(self, test_case_module_file_name, test_script_module_name):
        self.test_case_module = __import__(test_case_module_file_name)
        self.test_script_module = __import__(test_script_module_name) if test_script_module_name is not None else None

    def execute(self):
        n = 1
        success = 0
        for test in self.test_case_module.Test_Cases:
            print("Test case " + str(n) + ":")
            n += 1
            executable = True
            s = 1
            for name, action in test:
                action_status = action
                if action is None:
                    action_status = "not executable"
                    executable = False
                elif self.test_script_module is not None and action not in dir(self.test_script_module):
                    action_status = action + " not found in " + self.test_script_module.__name__
                    executable = False
                print(" Action " + str(s) + ": " + name + "(" + action_status + ")")
                s += 1

            test_result = "succeeded"
            if executable:
                try:
                    for name, action in test:
                        print(" Perform " + name + " by calling " + action)
                        if self.test_script_module is not None:
                            method = getattr(self.test_script_module, action)
                            method()
                        else:
                            print("  dummy done!")
                except:
                    print("  failed")
                    test_result = "failed"
            else:
                test_result = "failed"
            if test_result == "succeeded":
                success += 1
            print(test_result)
        print("Total success: " + str(success))






