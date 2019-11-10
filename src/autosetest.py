import gen_test_cases
import exec_test_cases


def main():
    gen_test_cases.init_test_cases_script()
    gen_test_cases.gen_all_test_cases()
    exec_test_cases.exec_all_test_cases()

main()