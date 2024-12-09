import importlib
import os
from dataclasses import dataclass
from typing import List, Optional

from consts import IO_TESTS_PREFIX, UNIT_TESTS_PREFIX, COMPARISON_TESTS_PREFIX, BONUS_TESTS_PREFIX, \
    P_COMPILATION_TESTS_PREFIX, N_COMPILATION_TESTS_PREFIX, AST_TESTS_PREFIX


@dataclass
class ExInfo:
    ex_base_dir: str

    ex_name: str # instead of EX_NUM
    required_src_files: list[str]
    required_hdr_files: list[str]
    required_other_files: list[str]
    optional_files: list[str]
    bonus_files: list[str]
    forbidden_files: list[str]
    submission_has_main: bool
    # [OPTIONAL] string containing preprocessor definition to pass in compilation command if bonus was
    # submitted. For example: "BONUS_SUBMITTED". Required if BONUS_FILES is not empty.
    bonus_macro: str

    presubmit_io_tests: List[int]
    presubmit_ast_tests: List[int]
    presubmit_unit_tests: List[int]
    presubmit_comparison_tests: List[int]
    presubmit_pcomp_tests: List[int]
    presubmit_ncomp_tests: List[int]

    # [OPTIONAL] Subset of Makefile Targets to execute for presubmit. For example: {all, lib}.
    presubmit_makefile_tests: List[str]

    presubmit_additional_srcs: List[str]
    autotests_additional_srcs: List[str]

    # [OPTIONAL] List of symbols to wrap during linkage. For each symbol in the list, all compiled
    #  programs MUST include a defined symbol with the name __wrap_<symbol>.
    #  For Example: ["malloc"], and then every compiled program MUST define a function called __wrap_malloc
    autotests_compilation_wrap_symbols: List[str]
    presubmit_compilation_wrap_symbols: List[str]

    # TODO bshor: should save prefixes as part of this class and compute these numbers based on autotests folder
    unit_tests_num: int
    comparison_tests_num: int
    bonus_tests_num: int
    io_tests_num: int
    p_compilation_tests_num: int
    n_compilation_tests_num: int
    ast_tests_num: int

    comparsion_script_path: str  # should be diff.py or starts_wth.py
    io_comparison_script_path: str
    ## deleted, maybe add later:
    ## should be part of python
    # comparison_script: str
    # comparison_student_output_path: str
    # io_comparison_script: str
    # io_student_output_path: str

    # """[OPTIONAL] Dictionary where keys are makefile targets and values are lists of files that should be
    # created by target. For example: {'all': ['some_file.o', 'some_program']} """
    makefile_tests: dict[str, List[str]]
    forbidden_functions: List[str]

    publish_school_solution: bool
    school_solution_additional_src: List[str]

    # TODO bshor: add lang as part of ex_info
    def get_lang(self):
        if self.ex_name in {"0", "1", "2", "3", 0, 1, 2, 3, "3a", "3b"}:
            return "C"
        return "C++"

    def get_school_sol_dir(self):
        return f"{self.ex_base_dir}/school_solution"

    def get_presub_src_dir(self):
        return f"{self.ex_base_dir}/presubmit_src"

    def get_presub_hdr_dir(self):
        return f"{self.ex_base_dir}/presubmit_headers"

    def get_autotests_src_dir(self):
        return f"{self.ex_base_dir}/autotest_src"

    def get_autotests_hdr_dir(self):
        return f"{self.ex_base_dir}/autotest_headers"

    def get_presubmit_include_dir(self):
        # include_dir used to be f"{courseBaseDir}/presubmit/{exName}/hdrs",
        # not sure why it was needed, I think because this is what shown to students
        return self.get_presub_hdr_dir()

    def get_presubmit_or_test_include_dir(self):
        if os.path.exists(self.get_autotests_hdr_dir()):
            return self.get_autotests_hdr_dir()
        return self.get_presub_hdr_dir()

    def get_presubmit_or_test_src_dir(self):
        if os.path.exists(self.get_autotests_src_dir()):
            return self.get_autotests_src_dir()
        return self.get_presub_src_dir()

    def get_presubmit_srcs(self):
        # return []

        srcs = []
        lang_ext = 'c' if self.get_lang() == "C" else 'cpp'
        if not self.submission_has_main:
            srcs.append(f"presubmit.{lang_ext}")
        for i in self.presubmit_additional_srcs:
            if i.endswith(".o") and not os.path.exists(f"{self.ex_base_dir}/presubmit_src/{i}"):
                srcs.append(i[:-2] + "." + lang_ext)
            else:
                srcs.append(i)

        return [f"{self.ex_base_dir}/presubmit_src/{i}" for i in srcs]


    # def get_presubmit_src_dir(self):
    #     return self.get_presub_src_dir()


def get_ex_info_from_folder(ex_folder: str) -> ExInfo:
    # use the import exercise_info to get the information, enable reimporting different exercise_info
    import sys
    sys.path.append(ex_folder)
    # exercise_info = None
    if "exercise_info" in sys.modules:
        # Re-import the module
        importlib.reload(sys.modules["exercise_info"])
    else:
        globals()["exercise_info"] = __import__("exercise_info")
    sys.path.remove(ex_folder)

    ex_base_dir = ex_folder

    # ex_name = os.path.basename(ex_folder).split("_")[1]
    ex_name = exercise_info.EX_NUM
    required_src_files = exercise_info.REQUIRED_SRC_FILES
    required_hdr_files = exercise_info.REQUIRED_HDR_FILES
    required_other_files = exercise_info.REQUIRED_OTHER_FILES
    optional_files = exercise_info.OPTIONAL_FILES
    bonus_files = exercise_info.BONUS_FILES
    assert len(bonus_files) == 0
    forbidden_files = exercise_info.FORBIDDEN_FILES
    submission_has_main = exercise_info.SUBMISSION_HAS_MAIN

    bonus_macro = exercise_info.BONUS_MACRO

    presubmit_io_tests = exercise_info.PRESUBMIT_IO_TESTS
    presubmit_ast_tests = exercise_info.PRESUBMIT_AST_TESTS
    presubmit_unit_tests = exercise_info.PRESUBMIT_UNIT_TESTS if hasattr(exercise_info, "PRESUBMIT_UNIT_TESTS") else []
    presubmit_comparison_tests = exercise_info.PRESUBMIT_COMPARISON_TESTS if hasattr(exercise_info, "PRESUBMIT_COMPARISON_TESTS") else []
    presubmit_makefile_tests = exercise_info.PRESUBMIT_MAKEFILE_TESTS if hasattr(exercise_info, "PRESUBMIT_MAKEFILE_TESTS") else []
    presubmit_pcomp_tests = exercise_info.PRESUBMIT_PCOMP_TESTS if hasattr(exercise_info, "PRESUBMIT_PCOMP_TESTS") else []
    presubmit_ncomp_tests = exercise_info.PRESUBMIT_NCOMP_TESTS if hasattr(exercise_info, "PRESUBMIT_NCOMP_TESTS") else []

    presubmit_additional_srcs = exercise_info.PRESUBMIT_ADDITIONAL_SRCS
    autotests_additional_srcs = exercise_info.AUTOTESTS_ADDITIONAL_SRCS
    autotests_compilation_wrap_symbols = exercise_info.AUTOTEST_COMPILATION_WRAP_SYMBOLS
    presubmit_compilation_wrap_symbols = exercise_info.PRESUBMIT_COMPILATION_WRAP_SYMBOLS if hasattr(exercise_info, "PRESUBMIT_COMPILATION_WRAP_SYMBOLS") else []

    # TODO bshor: this is abit of a hack to run on OSX (mac), where there is no wrap
    if sys.platform == "darwin": # check if MAC (OSX)
        print("******* ignoring wrap symbols for MAC ********")
        autotests_compilation_wrap_symbols = []
        presubmit_compilation_wrap_symbols = []
        presubmit_additional_srcs = [i for i in presubmit_additional_srcs if "wrap" not in i]
        presubmit_additional_srcs = [i for i in presubmit_additional_srcs if "malloc_helper" not in i]
        presubmit_additional_srcs = [i for i in presubmit_additional_srcs if "dynamic_allocation_helper" not in i]

    unit_tests_num = exercise_info.UNIT_TESTS_NUM
    comparison_tests_num = exercise_info.COMPARISON_TESTS_NUM
    bonus_tests_num = exercise_info.BONUS_TESTS_NUM
    io_tests_num = exercise_info.IO_TESTS_NUM
    p_compilation_tests_num = exercise_info.P_COMPILATION_TESTS_NUM
    n_compilation_tests_num = exercise_info.N_COMPILATION_TESTS_NUM
    ast_tests_num = exercise_info.AST_TESTS_NUM

    comparsion_script_path = exercise_info.COMPARISON_SCRIPT
    io_comparison_script_path = exercise_info.IO_COMPARISON_SCRIPT
    comparsion_scripts_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "comparsion_scripts")
    comparsion_script_path = os.path.join(comparsion_scripts_folder, comparsion_script_path)
    assert os.path.isfile(comparsion_script_path), f"comparsion_script_path {comparsion_script_path} not found"
    io_comparison_script_path = os.path.join(comparsion_scripts_folder, io_comparison_script_path)

    makefile_tests = exercise_info.MAKEFILE_TESTS
    forbidden_functions = exercise_info.FORBIDDEN_FUNCTIONS
    publish_school_solution = exercise_info.PUBLISH_SCHOOL_SOLUTION

    # notice there is a typo
    school_solution_additional_src = exercise_info.SCHOOL_SOLUTION_ADITIONAL_SRC if hasattr(exercise_info, "SCHOOL_SOLUTION_ADITIONAL_SRC") else []


    # lang_ext = 'c' if IS_C else 'cpp'
    # if not SUBMISSION_HAS_MAIN:
    #     additional_srcs += [f'{presubDir}/srcs/presubmit.{lang_ext}']
    return ExInfo(
        ex_base_dir=ex_base_dir,
        ex_name=ex_name,
        required_src_files=required_src_files,
        required_hdr_files=required_hdr_files,
        required_other_files=required_other_files,
        optional_files=optional_files,
        bonus_files=bonus_files,
        forbidden_files=forbidden_files,
        submission_has_main=submission_has_main,
        bonus_macro=bonus_macro,
        presubmit_io_tests=presubmit_io_tests,
        presubmit_ast_tests=presubmit_ast_tests,
        presubmit_unit_tests=presubmit_unit_tests,
        presubmit_comparison_tests=presubmit_comparison_tests,
        presubmit_pcomp_tests=presubmit_pcomp_tests,
        presubmit_ncomp_tests=presubmit_ncomp_tests,
        presubmit_makefile_tests=presubmit_makefile_tests,
        presubmit_additional_srcs=presubmit_additional_srcs,
        autotests_additional_srcs=autotests_additional_srcs,
        autotests_compilation_wrap_symbols=autotests_compilation_wrap_symbols,
        presubmit_compilation_wrap_symbols=presubmit_compilation_wrap_symbols,
        unit_tests_num=unit_tests_num,
        comparison_tests_num=comparison_tests_num,
        bonus_tests_num=bonus_tests_num,
        io_tests_num=io_tests_num,
        p_compilation_tests_num=p_compilation_tests_num,
        n_compilation_tests_num=n_compilation_tests_num,
        ast_tests_num=ast_tests_num,
        comparsion_script_path=comparsion_script_path,
        io_comparison_script_path=io_comparison_script_path,
        makefile_tests=makefile_tests,
        forbidden_functions=forbidden_functions,
        publish_school_solution=publish_school_solution,
        school_solution_additional_src=school_solution_additional_src,
    )


def create_cmake_file(ex_info: ExInfo, target_presubmit: str, target_school_sol_autotest: str,
                      target_school_sol_presubmit: str, output_cmake_path: str):
    strs = ["cmake_minimum_required(VERSION 3.12)\n"]
    strs.append(f"project(Ex{ex_info.ex_name})\n")

    standard = f"CMAKE_C_STANDARD 99" if ex_info.get_lang() == "C" else "CMAKE_CXX_STANDARD 14"
    strs.append(f"set({standard})\n\n")
    strs.append(f'include_directories({ex_info.get_school_sol_dir()})\n')
    school_sol_srcs = ' '.join([f'{ex_info.get_school_sol_dir()}/{src}' for src in ex_info.required_src_files])
    if ex_info.submission_has_main:
        strs.append(f"add_executable({target_school_sol_presubmit} {school_sol_srcs})")
    else:
        generated_presub_filename = "presubmit.c" if ex_info.get_lang() == "C" else "presubmit.cpp"
        presubmit_srcs_list = [f'{ex_info.get_presub_src_dir()}/{generated_presub_filename}']
        presubmit_srcs_list += [f'{ex_info.get_presub_src_dir()}/{src}' for src in ex_info.presubmit_additional_srcs]
        presubmit_srcs = " ".join(presubmit_srcs_list)
        strs.append(f"add_library({target_school_sol_presubmit} {school_sol_srcs})\n\n")
        strs.append(f"add_executable({target_presubmit} {presubmit_srcs})")
        strs.append(f"target_link_libraries({target_presubmit} m {target_school_sol_presubmit})")
        strs.append(f"target_include_directories({target_school_sol_presubmit} PUBLIC {ex_info.get_presub_hdr_dir()})\n\n")
        strs.append(f"target_include_directories({target_presubmit} PUBLIC {ex_info.get_presub_hdr_dir()})\n\n")

        strs.append(f"add_library({target_school_sol_autotest} {school_sol_srcs})\n\n")
        strs.append(f"target_include_directories({target_school_sol_autotest} PUBLIC {ex_info.get_autotests_hdr_dir()})\n\n")

        autotest_additional_srcs = ' '.join([f'{ex_info.get_autotests_src_dir()}/{src}'
                                             for src in ex_info.autotests_additional_srcs])

        def _get_str_for_test(number_of_tests, test_prefix):
            s = []
            for i in range(number_of_tests):
                target_name = f"{test_prefix}{i+1}"
                s.append(
                    f"add_executable({target_name} {ex_info.get_autotests_src_dir()}/{test_prefix}{i+1} {autotest_additional_srcs})")
                s.append(f"target_link_libraries({target_name} m {target_school_sol_autotest})")
                s.append(f"target_include_directories({target_name} PUBLIC {ex_info.get_autotests_hdr_dir()})\n\n")
            return s

        strs.extend(_get_str_for_test(ex_info.io_tests_num, IO_TESTS_PREFIX))
        strs.extend(_get_str_for_test(ex_info.unit_tests_num, UNIT_TESTS_PREFIX))
        strs.extend(_get_str_for_test(ex_info.comparison_tests_num, COMPARISON_TESTS_PREFIX))
        strs.extend(_get_str_for_test(ex_info.bonus_tests_num, BONUS_TESTS_PREFIX))
        strs.extend(_get_str_for_test(ex_info.p_compilation_tests_num, P_COMPILATION_TESTS_PREFIX))
        strs.extend(_get_str_for_test(ex_info.n_compilation_tests_num, N_COMPILATION_TESTS_PREFIX))
        strs.extend(_get_str_for_test(ex_info.ast_tests_num, AST_TESTS_PREFIX))

    # cmake_path = "CMakeLists.txt"
    if not os.path.isfile(output_cmake_path):
        print(f"Creating {output_cmake_path}...")
        with open(output_cmake_path, 'w') as cmk:
            cmk.write('\n'.join(strs))
    else:
        print(f"found existing file {output_cmake_path}, we don't want to overwrite it.")
        print("printing suggested cmakelists contents: ")
        print('\n'.join(strs))


def validate_ex_info(ex_info: ExInfo):
    print("Validating information")
    errors = ""
    school_sol_dir = ex_info.get_school_sol_dir()
    presubmit_dir = ex_info.get_presub_src_dir()
    autotests_dir = ex_info.get_autotests_src_dir()
    for f in ex_info.required_src_files:
        if not os.path.isfile(os.path.join(school_sol_dir, f)):
            errors += f"Error: Specified required source file {f} not found in directory {school_sol_dir}.\n"
    for f in ex_info.required_hdr_files:
        if not os.path.isfile(os.path.join(school_sol_dir, f)):
            errors += f"Error: Specified required header file {f} not found in directory {school_sol_dir}.\n"
    for f in ex_info.bonus_files:
        if not os.path.isfile(os.path.join(school_sol_dir, f)):
            errors += f"Error: Specified bonus file {f} not found in directory {school_sol_dir}.\n"
    if ex_info.bonus_files and not ex_info.bonus_macro:
        errors += f"Error: Specified files for bonus submissions but no preprocessor definition.\n"
    for f in ex_info.presubmit_additional_srcs:
        if not os.path.isfile(os.path.join(presubmit_dir, f)):
            errors += f"Error: Specified presubmit additinal source file {f} not found in directory {presubmit_dir}.\n"
    if ex_info.submission_has_main:
        if not ex_info.io_tests_num:
            errors += f"Error: If the submission includes a main function, I/O tests must be used.\n"
        if len(ex_info.presubmit_io_tests) == 0:
            errors += f"Warning: No I/O Tests for presubmit means it will only check compilation.\n"
    if not ex_info.submission_has_main \
            and not os.path.isfile(os.path.join(presubmit_dir, "presubmit.c")) \
            and not os.path.isfile(os.path.join(presubmit_dir, "presubmit.cpp")):
        errors += f"Error: Main presubmit source file (presubmit.c/cpp) not found in directory {presubmit_dir}.\n"
    for f in ex_info.autotests_additional_srcs:
        if not os.path.isfile(os.path.join(autotests_dir, f)):
            errors += f"Error: Specified autotests additinal source file {f} not found in directory {autotests_dir}.\n"

    def _validate_tests(test_num, test_prefix, test_dir):
        e = []
        for i in range(1, test_num + 1):
            if not os.path.isfile(os.path.join(test_dir, f"{test_prefix}{i}.c")) \
                    and not os.path.isfile(os.path.join(test_dir, f"{test_prefix}{i}.cpp")):
                e += f"Error: Specified {test_num} {test_prefix} tests, but {test_prefix}{i} was not found in directory {test_dir}.\n"
        return e

    errors += _validate_tests(ex_info.io_tests_num, IO_TESTS_PREFIX, autotests_dir)
    errors += _validate_tests(ex_info.unit_tests_num, UNIT_TESTS_PREFIX, autotests_dir)
    errors += _validate_tests(ex_info.comparison_tests_num, COMPARISON_TESTS_PREFIX, autotests_dir)
    errors += _validate_tests(ex_info.bonus_tests_num, BONUS_TESTS_PREFIX, autotests_dir)
    errors += _validate_tests(ex_info.p_compilation_tests_num, P_COMPILATION_TESTS_PREFIX, autotests_dir)
    errors += _validate_tests(ex_info.n_compilation_tests_num, N_COMPILATION_TESTS_PREFIX, autotests_dir)
    errors += _validate_tests(ex_info.ast_tests_num, AST_TESTS_PREFIX, autotests_dir)

    def _validate_presubmit_numbering(test_name, test_num, presubmit_tests):
        if len(presubmit_tests) == 0:
            return []
        if max(presubmit_tests) > test_num:
            return [f"Error: Presubmit specifies {test_name} test {max(presubmit_tests)}, "
                    f"but the number of specified I/O tests is {test_num}\n"]
        return []

    errors += _validate_presubmit_numbering("I/O", ex_info.io_tests_num, ex_info.presubmit_io_tests)
    errors += _validate_presubmit_numbering("Unit", ex_info.unit_tests_num, ex_info.presubmit_unit_tests)
    errors += _validate_presubmit_numbering("Comparison", ex_info.comparison_tests_num, ex_info.presubmit_comparison_tests)
    errors += _validate_presubmit_numbering("P Compilation", ex_info.p_compilation_tests_num, ex_info.presubmit_pcomp_tests)
    errors += _validate_presubmit_numbering("N Compilation", ex_info.n_compilation_tests_num, ex_info.presubmit_ncomp_tests)
    errors += _validate_presubmit_numbering("AST", ex_info.ast_tests_num, ex_info.presubmit_ast_tests)

    if not os.path.isfile(os.path.join("errorcodes", f"{ex_info.ex_name}.errorcodes")):
        errors += f"Error: file {ex_info.ex_name}.errorcodes not found in errorcodes\n"
    if ex_info.makefile_tests:
        if 'makefile' not in ex_info.required_other_files and 'Makefile' not in ex_info.required_other_files:
            errors += f"Error: specified makefile tests, but REQUIRED_OTHER_FILES does not specify a " \
                      f"makefile\n"
    if errors:
        print("Found some errors:\n", errors)
        return False
    print("Validation Successful!")
    return True


if __name__ == "__main__":
    print(get_ex_info_from_folder("/Users/benshor/Documents/Data/202410_cpp_job/repos/labcc_ex1"))