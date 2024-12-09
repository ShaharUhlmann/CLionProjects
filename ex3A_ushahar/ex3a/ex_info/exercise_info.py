#!/usr/bin/python3
import datetime
import os.path

from constants import *

"""
Fill in the required information in this file.
Once filled in, you may run the script and it will let you know if everything is in order.
"""

#############################################################################################################
######################################### Your information goes here ########################################
#############################################################################################################

EX_NUM = '3a'
"""[REQUIRED] Exercise Number. 1-6"""

REQUIRED_SRC_FILES = ["markov_chain.c", "tweets_generator.c"]
"""[REQUIRED] List of Required Source Files In Submission. For example: ["file1.c", "file2.c"]"""

REQUIRED_HDR_FILES = ["markov_chain.h"]
"""[REQUIRED] List of Required Header Files In Submission. For example: ["file1.h", "file2.h"]"""

REQUIRED_OTHER_FILES = []
"""[REQUIRED] List of Required Header Files In Submission. For example: ["file1", "file2"]"""

OPTIONAL_FILES = []
"""[OPTIONAL] List of Optional Files In Submission. For example: ["optional.c"]. May be an empty list."""

BONUS_FILES = []
"""[OPTIONAL] List of Required Files For Bonus Submission. For example: ["bonus.c"]. May be an empty list"""

FORBIDDEN_FILES = ["linked_list.c", "linked_list.h"]
"""[OPTIONAL] List of Forbidden Files In Submission. For example: ["main.c"]. May be an empty list."""

SUBMISSION_HAS_MAIN = True
"""[REQUIRED] boolean describing whether or not the students' submission contains a main method."""

BONUS_MACRO = ""
"""[OPTIONAL] string containing preprocessor definition to pass in compilation command if bonus was 
submitted. For example: "BONUS_SUBMITTED". Required if BONUS_FILES is not empty."""

PRESUBMIT_IO_TESTS = {1,2,3}
"""[OPTIONAL] Subset of IOTests to preform for presubmit. Only if students' submission contains a main
 method. For example: {1, 3, 7}."""

PRESUBMIT_AST_TESTS = {1,2,3,4,5,6,7,8}
"""[OPTIONAL] Subset of AST Tests to preform for presubmit. For example: {1, 3, 7}."""

PRESUBMIT_UNIT_TESTS = {}
"""[OPTIONAL] Subset of UNIT Tests to preform for presubmit. For example: {1, 3, 7}."""

PRESUBMIT_COMPARISON_TESTS = {}
"""[OPTIONAL] Subset of comparison Tests to preform for presubmit. For example: {1, 3, 7}."""

PRESUBMIT_PCOMP_TESTS = {}
"""[OPTIONAL] Subset of PCOMP Tests to preform for presubmit. For example: {1, 3, 7}."""

PRESUBMIT_NCOMP_TESTS = {}
"""[OPTIONAL] Subset of NCOMP Tests to preform for presubmit. For example: {1, 3, 7}."""

PRESUBMIT_MAKEFILE_TESTS = {}
"""[OPTIONAL] Subset of Makefile Targets to execute for presubmit. For example: {all, lib}."""

PRESUBMIT_ADDITIONAL_SRCS = ["linked_list.c"]
"""[OPTIONAL] List of Additional Presubmit Sources For example: ["Presubmit_helper.c"]"""

AUTOTESTS_ADDITIONAL_SRCS = ["linked_list.c"]
"""[OPTIONAL] List of Autotests Additional Sources. For example: ["autotest_helper.c"]"""

AUTOTEST_COMPILATION_WRAP_SYMBOLS = []
"""[OPTIONAL] List of symbols to wrap during linkage. For each symbol in the list, all compiled
 programs MUST include a defined symbol with the name __wrap_<symbol>.
 For Example: ["malloc"], and then every compiled program MUST define a function called __wrap_malloc"""

PRESUBMIT_COMPILATION_WRAP_SYMBOLS = []
"""[OPTIONAL] List of symbols to wrap during linkage. For each symbol in the list, all compiled
 programs MUST include a defined symbol with the name __wrap_<symbol>.
 For Example: ["malloc"], and then every compiled program MUST define a function called __wrap_malloc"""

UNIT_TESTS_NUM = 0
"""[OPTIONAL] Number of Standalone Tests. 0 if none."""

COMPARISON_TESTS_NUM = 0
"""[OPTIONAL] Number of Comparison Tests. 0 if none."""

COMPARISON_SCRIPT = "diff.py"
"""[REQUIRED FOR PREVIOUS OPTION] string containing the name of a python script that receives 2 arguments.
    For example: "compare.py" ."""

COMPARISON_STUDENT_OUTPUT_PATH = ""
"""[OPTIONAL] string containing prefix path to student output file, if previous option was FILE. 
The test number will be appended after the prefix. For example: "stu_out_" means the output for test number
# will be found at stu_out_# """

MAKEFILE_TESTS = {}
"""[OPTIONAL] Dictionary where keys are makefile targets and values are lists of files that should be 
created by target. For example: {'all': ['some_file.o', 'some_program']} """

BONUS_TESTS_NUM = 0
"""[OPTIONAL] Number of Bonus Tests. 0 if none"""

IO_TESTS_NUM = 3
"""[OPTIONAL] Number of IO Tests. 0 if none."""

IO_COMPARISON_SCRIPT = "diff.py"
"""[REQUIRED FOR PREVIOUS OPTION] string containing the name of a python script that receives 2 arguments.
    For example: "compare.py" ."""

IO_STUDENT_OUTPUT_PATH = ""
"""[OPTIONAL] string containing prefix path to student output file, if previous option was FILE. 
The test number will be appended after the prefix. For example: "stu_out_" means the output for test number
# will be found at stu_out_# """

P_COMPILATION_TESTS_NUM = 0
"""[OPTIONAL] Number of Positive Compilation Tests. 0 if none."""

N_COMPILATION_TESTS_NUM = 0
"""[OPTIONAL] Number of Negative Compilation Tests. 0 if none"""

AST_TESTS_NUM = 8
"""[OPTIONAL] Number of AST Tests. 0 if none"""

FORBIDDEN_FUNCTIONS = ["scanf", "fscanf", "exit", "atoi"]
"""List of forbidden functions for exercise."""

PUBLISH_SCHOOL_SOLUTION = True
"""[OPTIONAL] Make a compiled version of the school solution available to students. Currently only 
supported for exercises with main."""

SCHOOL_SOLUTION_ADITIONAL_SRC = ["linked_list.c"]
"""[OPTIONAL] src needed for school solution."""

SUBMISSION_DEADLINE = datetime.datetime(year=2024, month=12, day=11, hour=23, minute=59)
"""Date of submission deadline, used in order to calculate early submission bonuses 
(most likely only need to change month and day)"""

#############################################################################################################
######################################### No need to read past this #########################################
#############################################################################################################

def create_cmake_file():

    TARGET_SCHOOL_SOL_PRESUB = 'school_solution_presub'
    TARGET_SCHOOL_SOL_AUTOTEST = 'school_solution_autotest'
    TARGET_PRESUBMIT = 'presubmit'

    strs = ["cmake_minimum_required(VERSION 3.12)\n"]
    strs.append(f"project(Ex{EX_NUM})\n")
    lang = 'C' if EX_NUM < 4 else 'CXX'
    standard = f"CMAKE_{lang}_STANDARD {99 if lang == 'C' else 14}"
    strs.append(f"set({standard})\n\n")
    strs.append(f'include_directories({DIR_SCHOOL_SOL})\n')
    school_sol_srcs = ' '.join([f'{DIR_SCHOOL_SOL}/{src}' for src in REQUIRED_SRC_FILES])
    if SUBMISSION_HAS_MAIN:
        strs.append(f"add_executable({TARGET_SCHOOL_SOL_PRESUB} {school_sol_srcs})")
    else:
        presubmit_srcs = ' '.join([f'{DIR_PRESUB_SRC}/presubmit.c{"pp" if lang != "C" else ""}']+[f'{DIR_PRESUB_SRC}/{src}' for src in PRESUBMIT_ADDITIONAL_SRCS])
        strs.append(f"add_library({TARGET_SCHOOL_SOL_PRESUB} {school_sol_srcs})\n\n")
        strs.append(f"add_executable({TARGET_PRESUBMIT} {presubmit_srcs})")
        strs.append(f"target_link_libraries({TARGET_PRESUBMIT} m {TARGET_SCHOOL_SOL_PRESUB})")
        strs.append(f"target_include_directories({TARGET_SCHOOL_SOL_PRESUB} PUBLIC {DIR_PRESUB_HDR})\n\n")
        strs.append(f"target_include_directories({TARGET_PRESUBMIT} PUBLIC {DIR_PRESUB_HDR})\n\n")

        strs.append(f"add_library({TARGET_SCHOOL_SOL_AUTOTEST} {school_sol_srcs})\n\n")
        strs.append(f"target_include_directories({TARGET_SCHOOL_SOL_AUTOTEST} PUBLIC {DIR_AUTOTESTS_HDR})\n\n")

        autotest_additional_srcs = ' '.join([f'{DIR_AUTOTESTS_SRC}/{src}' for src in AUTOTESTS_ADDITIONAL_SRCS])

        for i in range(1, UNIT_TESTS_NUM + 1):
            target_name = f"{UNIT_TESTS_PREFIX}{i}"
            strs.append(f"add_executable({target_name} {DIR_AUTOTESTS_SRC}/{UNIT_TESTS_PREFIX}{i} {autotest_additional_srcs})")
            strs.append(f"target_link_libraries({target_name} m {TARGET_SCHOOL_SOL_AUTOTEST})")
            strs.append(f"target_include_directories({target_name} PUBLIC {DIR_AUTOTESTS_HDR})\n\n")



        for i in range(1, COMPARISON_TESTS_NUM + 1):
            target_name = f"{COMPARISON_TESTS_PREFIX}{i}"
            strs.append(f"add_executable({target_name} {DIR_AUTOTESTS_SRC}/{COMPARISON_TESTS_PREFIX}{i} {autotest_additional_srcs})")
            strs.append(f"target_link_libraries({target_name} m {TARGET_SCHOOL_SOL_AUTOTEST})")
            strs.append(f"target_include_directories({target_name} PUBLIC {DIR_AUTOTESTS_HDR})\n\n")

        for i in range(1, P_COMPILATION_TESTS_NUM + 1):
            target_name = f"{P_COMPILATION_TESTS_PREFIX}{i}"
            strs.append(f"add_executable({target_name} {DIR_AUTOTESTS_SRC}/{P_COMPILATION_TESTS_PREFIX}{i} {autotest_additional_srcs})")
            strs.append(f"target_link_libraries({target_name} m {TARGET_SCHOOL_SOL_AUTOTEST})")
            strs.append(f"target_include_directories({target_name} PUBLIC {DIR_AUTOTESTS_HDR})\n\n")

        for i in range(1, N_COMPILATION_TESTS_NUM + 1):
            target_name = f"{N_COMPILATION_TESTS_PREFIX}{i}"
            strs.append(f"add_executable({target_name} {DIR_AUTOTESTS_SRC}/{N_COMPILATION_TESTS_PREFIX}{i} {autotest_additional_srcs})")
            strs.append(f"target_link_libraries({target_name} m {TARGET_SCHOOL_SOL_AUTOTEST})")
            strs.append(f"target_include_directories({target_name} PUBLIC {DIR_AUTOTESTS_HDR})\n\n")

    cmake_path = "CMakeLists.txt"
    if not os.path.isfile(cmake_path):
        print(f"Creating {cmake_path}...")
        with open(cmake_path, 'w') as cmk:
            cmk.write('\n'.join(strs))
    else:
        print(f"found existing file {cmake_path}, we don't want to overwrite it.")
        print("printing suggested cmakelists contents: ")
        print('\n'.join(strs))


if __name__ == '__main__':
    print("Validating information")
    errors = ""
    if EX_NUM not in [1, 2, 3, 4, 5, 6]:
        errors += f"Error: Specified EX_NUM: {EX_NUM} is invalid (must be a number between 1 and 6).\n"
    for f in REQUIRED_SRC_FILES:
        if not os.path.isfile(os.path.join(DIR_SCHOOL_SOL, f)):
            errors += f"Error: Specified required source file {f} not found in directory {DIR_SCHOOL_SOL}.\n"
    for f in REQUIRED_SRC_FILES:
        if not os.path.isfile(os.path.join(DIR_SCHOOL_SOL, f)):
            errors += f"Error: Specified required header file {f} not found in directory {DIR_SCHOOL_SOL}.\n"
    for f in BONUS_FILES:
        if not os.path.isfile(os.path.join(DIR_SCHOOL_SOL, f)):
            errors += f"Error: Specified bonus file {f} not found in directory {DIR_SCHOOL_SOL}.\n"
    if BONUS_FILES and not BONUS_MACRO:
        errors += f"Error: Specified files for bonus submissions but no preprocessor definition.\n"
    for f in PRESUBMIT_ADDITIONAL_SRCS:
        if not os.path.isfile(os.path.join(DIR_PRESUB_SRC, f)):
            errors += f"Error: Specified presubmit additinal source file {f} not found in directory {DIR_PRESUB_SRC}.\n"
    if SUBMISSION_HAS_MAIN:
        if not IO_TESTS_NUM:
            errors += f"Error: If the submission includes a main function, I/O tests must be used.\n"
        if not PRESUBMIT_IO_TESTS:
            errors += f"Warning: No I/O Tests for presubmit means it will only check compilation.\n"
        if max(PRESUBMIT_IO_TESTS) > IO_TESTS_NUM:
            errors += f"Error: Presubmit specifies I/O test {max(PRESUBMIT_IO_TESTS)}, but the number of specified I/O tests is {IO_TESTS_NUM}\n"
    if not SUBMISSION_HAS_MAIN and not os.path.isfile(
            os.path.join(DIR_PRESUB_SRC, "presubmit.c")) and not os.path.isfile(
        os.path.join(DIR_PRESUB_SRC, "presubmit.cpp")):
        errors += f"Error: Main presubmit source file (presubmit.c/cpp) not found in directory {DIR_PRESUB_SRC}.\n"
    for f in AUTOTESTS_ADDITIONAL_SRCS:
        if not os.path.isfile(os.path.join(DIR_AUTOTESTS_SRC, f)):
            errors += f"Error: Specified autotests additinal source file {f} not found in directory {DIR_AUTOTESTS_SRC}.\n"
    for i in range(1, UNIT_TESTS_NUM + 1):
        if not os.path.isfile(
                os.path.join(DIR_AUTOTESTS_SRC, f"{UNIT_TESTS_PREFIX}{i}.c")) and not os.path.isfile(
            os.path.join(DIR_AUTOTESTS_SRC, f"{UNIT_TESTS_PREFIX}{i}.cpp")):
            errors += f"Error: Specified {UNIT_TESTS_NUM} unit tests, but {UNIT_TESTS_PREFIX}{i}  was not found in directory {DIR_AUTOTESTS_SRC}.\n"
    for i in range(1, COMPARISON_TESTS_NUM + 1):
        if not os.path.isfile(
                os.path.join(DIR_AUTOTESTS_SRC, f"{COMPARISON_TESTS_PREFIX}{i}.c")) and not os.path.isfile(
            os.path.join(DIR_AUTOTESTS_SRC, f"{COMPARISON_TESTS_PREFIX}{i}.cpp")):
            errors += f"Error: Specified {COMPARISON_TESTS_NUM} comparison tests, but {COMPARISON_TESTS_PREFIX}{i}  was not found in directory {DIR_AUTOTESTS_SRC}.\n"
    for i in range(1, P_COMPILATION_TESTS_NUM + 1):
        if not os.path.isfile(os.path.join(DIR_AUTOTESTS_SRC,
                                           f"{P_COMPILATION_TESTS_PREFIX}{i}.c")) and not os.path.isfile(
            os.path.join(DIR_AUTOTESTS_SRC, f"{P_COMPILATION_TESTS_PREFIX}{i}.cpp")):
            errors += f"Error: Specified {P_COMPILATION_TESTS_NUM} p_compilation tests, but {P_COMPILATION_TESTS_PREFIX}{i}  was not found in directory {DIR_AUTOTESTS_SRC}.\n"
    for i in range(1, N_COMPILATION_TESTS_NUM + 1):
        if not os.path.isfile(os.path.join(DIR_AUTOTESTS_SRC,
                                           f"{N_COMPILATION_TESTS_PREFIX}{i}.c")) and not os.path.isfile(
            os.path.join(DIR_AUTOTESTS_SRC, f"{N_COMPILATION_TESTS_PREFIX}{i}.cpp")):
            errors += f"Error: Specified {N_COMPILATION_TESTS_NUM} n_compilation tests, but {N_COMPILATION_TESTS_PREFIX}{i}  was not found in directory {DIR_AUTOTESTS_SRC}.\n"
    for i in range(1, AST_TESTS_NUM + 1):
        if not os.path.isfile(os.path.join(DIR_AUTOTESTS_SRC, f"{AST_TESTS_PREFIX}{i}.match")):
            errors += f"Error: Specified {AST_TESTS_NUM} AST tests, but {AST_TESTS_PREFIX}{i}.match  was not found in directory {DIR_AUTOTESTS_SRC}.\n"
    if PRESUBMIT_AST_TESTS and max(PRESUBMIT_AST_TESTS) > AST_TESTS_NUM:
        errors += f"Error: Presubmit specifies AST test {max(PRESUBMIT_AST_TESTS)}, but the number of specified AST tests is {AST_TESTS_NUM}\n"
    if not os.path.isfile(os.path.join(DIR_ERRORCODES, f"ex{EX_NUM}.errorcodes")):
        errors += f"Error: file ex{EX_NUM}.errorcodes not found in {DIR_ERRORCODES}\n"
    if MAKEFILE_TESTS:
        if 'makefile' not in REQUIRED_OTHER_FILES and 'Makefile' not in REQUIRED_OTHER_FILES:
            errors += f"Error: specified makefile tests, but REQUIRED_OTHER_FILES does not specify a " \
                      f"makefile\n"
    if errors:
        print("Found some errors:\n", errors)
    else:
        print("Validation Successful!")
        create_cmake_file()
