#! /usr/bin/python3
import sys
from typing import Optional

import common_tests
from common_tests import UserLogger
from consts import PRESUBMIT_FAILED_MESSAGE
import ex_info_wrap
from env_consts import CLANG_TIDY_PATH, CLANG_QUERY_PATH
from ex_info_wrap import ExInfo
import os


def run_all_tests(ex_info: ExInfo, temp_dir: str, logger: UserLogger, executable_name: Optional[str] = None):
    print("\n=====================")
    print(" Public test cases")
    print("=====================\n")

    if CLANG_QUERY_PATH is not None:
        common_tests.run_ast_tests(ex_info, temp_dir, logger, ex_info.presubmit_ast_tests)
    else:
        print("******** clang-query not found in PATH. Skipping AST tests ********")
    common_tests.run_makefile_tests(ex_info, temp_dir, logger, ex_info.makefile_tests)
    if ex_info.submission_has_main:
        assert executable_name is not None, "Missing executable name for submission with main"
        common_tests.run_io_tests(ex_info, temp_dir, executable_name, logger, ex_info.presubmit_io_tests)
    else:
        common_tests.run_pcomp_tests(ex_info, temp_dir, logger, ex_info.presubmit_pcomp_tests)
        common_tests.run_ncomp_tests(ex_info, temp_dir, logger, ex_info.presubmit_ncomp_tests)
        common_tests.run_unit_tests(ex_info, temp_dir, logger, ex_info.presubmit_unit_tests)
        common_tests.run_comparsion_tests(ex_info, temp_dir, logger, ex_info.presubmit_comparison_tests, False)
        common_tests.run_presubmit_tests(ex_info, temp_dir, logger, executable_name)

    passed_test_exists = any(logger.test_results)
    failed_test_exists = any(not res for res in logger.test_results)

    # Presubmit fails if all tests failed (by course' guidelines)
    if passed_test_exists or len(logger.test_results) == 0:
        if failed_test_exists:
            print("""*****************************************
*                   *                   *
*        Passed Preusbmission,          *
*     but some problems detected.       *
*        Fix them for full marks        *
*                   *                   *
*****************************************""")
            # sys.exit(0)
        else:
            print("""*****************************************
*                  ***                  *
*          Passed all tests!!           *
*              Good Job!                *
*                  ***                  *
*****************************************""")

    else:
        print(PRESUBMIT_FAILED_MESSAGE)


def run_presubmit(ex_folder, tar_file):
    ex_info = ex_info_wrap.get_ex_info_from_folder(ex_folder)
    logger = UserLogger("/dev/null", None)
    temp_dir = common_tests.extract_to_temp_dir(tar_file, logger)
    common_tests.validate_files_in_dir(ex_info, temp_dir, logger)
    bonus_submitted = common_tests.check_has_bonus(ex_info, temp_dir, logger)

    if CLANG_TIDY_PATH is not None and CLANG_QUERY_PATH is not None:
        common_tests.check_forbidden_functions(ex_info, temp_dir, logger)
        common_tests.check_coding_style(ex_info, temp_dir, logger)
    else:
        print("******** clang-tidy or clang-query not found in PATH. Skipping coding style tests ********")

    executable_name = "test"
    common_tests.compile_code(ex_info, bonus_submitted, executable_name, logger)

    run_all_tests(ex_info, temp_dir, logger, executable_name)


def usage():
    scriptName = os.path.split(sys.argv[0])[1]
    print(scriptName + " <ex_repo_folder> <tar_file>")
    print("Will test the given tar file as a candidate submission for the exercise.")
    print("Example:\n\t" + scriptName + " ex.tar")

    print("""Note: passing this test script does not guarantee a high grade.
These are only very basic tests to avoid some common mistakes.
If an error is found, correct it and run the script on the corrected file to make sure it is ok.
""")


def main():
    # check that a file was supplied.
    if len(sys.argv) not in [3]:
        usage()
        sys.exit(1)

    # input_is_git = not (len(sys.argv) == 4 and sys.argv[3] == "nogit")

    print("\nRunning presubmission script...\n\n")
    # argv[1] is the name of the candidate submission file. e.g. "ex3.tar"
    ex_folder = os.path.abspath(sys.argv[1])
    tar_file = os.path.abspath(sys.argv[2])

    run_presubmit(ex_folder, tar_file)


if __name__ == "__main__":
    main()
    # print("Running Ex1")
    # run_presubmit(ex_folder="/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex1",
    #               tar_file="/Users/benshor/Documents/Data/202410_cpp_job/ex1-test3/ex1.tar"
    #               # tar_file="/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex1/school_solution_filtered"
    #               )
    # print("Running Ex2")
    # run_presubmit(ex_folder="/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex2",
    #               tar_file="/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex2/school_solution_filtered"
    #               )
    #
    # # # Bad IO tests because rand seems to be different in MAC and linux
    # print("Running Ex3")
    # run_presubmit(ex_folder="/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex3a",
    #               tar_file="/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex3a/school_solution_filtered"
    #               )
    # run_presubmit(ex_folder="/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex3b",
    #               tar_file="/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex3b/school_solution_filtered"
    #               )
    # print("Running Ex4")
    # run_presubmit(ex_folder="/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex4",
    #               tar_file="/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex4/school_solution_filtered"
    #               )
    # print("Running Ex5")
    # run_presubmit(ex_folder="/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex5",
    #               tar_file="/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex5/school_solution_filtered"
    #               )




