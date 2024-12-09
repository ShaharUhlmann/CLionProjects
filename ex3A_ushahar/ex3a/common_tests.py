import os
import sys
from datetime import datetime
from typing import Optional, List
from xml.etree.ElementTree import ElementTree

import ps_utils
from consts import PRESUBMIT_FAILED_MESSAGE, ALLOWED_CODING_STYLE_ERRORS, IGNORE_CODINGSTYLE_ERRORS, \
    NO_SUM_CODING_STYLE_ERRORS, MAX_CODINGSTYLE_PENALTY, AST_TESTS_PREFIX, AST_TESTS_ERRORCODE_PREFIX, MAX_SECS_TEST, \
    MAKEFILE_TESTS_ERRORCODE_PREFIX, IO_STUDENT_OUTPUT_PATH_PREFIX, IO_TESTS_PREFIX, SEGFAULT_CODES, \
    IO_TESTS_ERRORCODE_PREFIX, VALGRIND_TYPE_TO_ERRORCODE_DICT, COMPARISON_TESTS_PREFIX, \
    COMPARISON_STUDENT_OUTPUT_PATH_PREFIX, COMPARISON_TESTS_ERRORCODE_PREFIX, P_COMPILATION_TESTS_PREFIX, \
    N_COMPILATION_TESTS_PREFIX, UNIT_TESTS_PREFIX, UNIT_TESTS_ERRORCODES_PREFIX, PRESUBMIT_INPUTS_PREFIX_FORMAT, \
    PRESUBMISSION_TESTS_ERRORCODE_PREFIX
from env_consts import OVERRIDE_SCHOOL_OUTPUT_FOLDER
from ex_info_wrap import ExInfo


def _get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class UserLogger:
    def __init__(self, error_code_output_path, debug_output_folder: Optional[str], disable_prints=False):
        self.output_path = error_code_output_path
        self.error_code_file = open(error_code_output_path, 'a')

        if debug_output_folder:
            self.debug_output_folder = debug_output_folder
            os.makedirs(debug_output_folder, exist_ok=True)
            debug_output_path = os.path.join(debug_output_folder, "debug.log")
            self.debug_file = open(debug_output_path, 'a', encoding='utf-8', errors='replace')
            self.debug_file.write(f"Starting Debug for {error_code_output_path} {_get_timestamp()}\n")
        else:
            self.debug_output_folder = None
            self.debug_file = sys.stdout
        self.disable_prints = disable_prints
        self.closed = False
        self.test_results = []
        self.segfault_counter = 0
        self.valgrind_error_count = dict()

    def add_test_result(self, result: bool):
        self.test_results.append(result)

    def write_error_code(self, error_code: str):
        self.error_code_file.write(f"\t{error_code}\n")

    def add_valgrind_error(self, error_code: str):
        if error_code not in self.valgrind_error_count:
            self.valgrind_error_count[error_code] = 0
        self.valgrind_error_count[error_code] += 1

    def write_user_name(self, name: str):
        self.error_code_file.write(f"{name}:\n")

    def end_user(self):
        pass

    def debug(self, files, log_message=""):
        if self.debug_output_folder:
            for file in files:
                os.system(f'cp "{file}" "{self.debug_output_folder}/"')
        if log_message:
            self.debug_file.write(f"{log_message}\n")
            if not self.disable_prints and self.debug_file != sys.stdout:
                print(log_message)

    def write_debug(self, *args):
        log_message = " ".join(map(str, args))
        self.debug_file.write(f"{log_message}\n")
        if not self.disable_prints and self.debug_file != sys.stdout:
            print(log_message)

    def close(self):
        self.error_code_file.close()
        self.closed = True


class BadSubmissionException(Exception):
    pass


def extract_to_temp_dir(submission_path: str, logger: UserLogger) -> str:
    # submission_path can be folder or tar file
    # returns path to tmp dir with extracted files
    temp_dir = ps_utils.createTempDir("labcc_temp")
    os.chdir(temp_dir)

    if os.path.isdir(submission_path):
        os.system(f'cp -rf "{submission_path}"/* .')
        logger.write_debug("files in dir", os.listdir(temp_dir))
        return temp_dir

    # Open tar file
    if ps_utils.extractTar(submission_path, disable_print=logger.disable_prints):
        logger.write_debug(PRESUBMIT_FAILED_MESSAGE)
        logger.write_error_code("BAD_SUBMISSION{Failed to extract tar file}")
        raise BadSubmissionException("Failed to extract tar file")

    logger.write_debug("Tar extracted O.K.")
    logger.write_debug(f"For your convenience, the MD5 checksum "
                       f"for your submission is {ps_utils.md5checksum(submission_path)}")

    logger.write_debug("Files in tar file", os.listdir(temp_dir))
    if len(os.listdir(temp_dir)) == 1:
        possible_dir = os.listdir(temp_dir)[0]
        if os.path.isdir(possible_dir):
            os.system(f"cp -rf \"{possible_dir}\"/* .")
            os.system(f"rm -rf \"{possible_dir}\"")
            logger.write_debug("files in tar only dir", os.listdir(temp_dir))
    return temp_dir


def validate_files_in_dir(ex_info: ExInfo, temp_dir: str, logger: UserLogger):
    logger.write_debug("Running validation of files")
    # Make sure the files are as they should be.
    required = ex_info.required_src_files + ex_info.required_hdr_files + ex_info.required_other_files
    good_patterns = ["README.md"] + ex_info.optional_files + ex_info.bonus_files + required
    if ps_utils.checkFiles(temp_dir,
                           requiredFiles=required,
                           notPermitedFiles=ex_info.forbidden_files,
                           goodPatterns=good_patterns,
                           badPatterns=["*.py", "*.pyc"],
                           disable_print=logger.disable_prints
                           ):
        logger.write_debug(PRESUBMIT_FAILED_MESSAGE)
        logger.write_error_code("BAD_SUBMISSION{Missing or forbidden files in submission.}")
        raise BadSubmissionException("Missing or forbidden files in submission.")

    # Make sure there are no empty files submitted
    # (we do this since these can be compiled without error)
    if ps_utils.emptyFiles(temp_dir, disable_print=logger.disable_prints):
        logger.write_debug(PRESUBMIT_FAILED_MESSAGE)
        logger.write_error_code("BAD_SUBMISSION{Empty files in submission.}")
        raise BadSubmissionException("Empty files in submission.")


def check_has_bonus(ex_info: ExInfo, tempDir: str, logger: UserLogger) -> bool:
    if ex_info.bonus_tests_num == 0:
        return False

    logger.write_debug("Checking if bonus was submitted...")
    bonus_submitted = not ps_utils.checkFiles(tempDir, ex_info.bonus_files, [], ["*.*", "*"], [],
                                              disable_print=logger.disable_prints)
    if bonus_submitted:
        logger.write_debug(f"Found bonus submission: {ex_info.bonus_files}")
    else:
        logger.write_debug("Bonus not submitted")
    return bonus_submitted


def check_forbidden_functions(ex_info: ExInfo, temp_dir: str, logger: UserLogger):
    for func in ex_info.forbidden_functions:
        if ps_utils.checkASTFucntionUsageExists(temp_dir,
                                                src_files=ex_info.required_src_files,
                                                include_dir=ex_info.get_presubmit_or_test_include_dir(),
                                                function_name=func,
                                                lang=ex_info.get_lang()):
            logger.write_debug(f"Found usage of forbidden function: {func}")
            logger.write_debug(PRESUBMIT_FAILED_MESSAGE)
            logger.write_error_code(f"forbidden_function{{forbidden function called: {func}}}")
            raise BadSubmissionException("forbidden_function")


def check_coding_style(ex_info: ExInfo, temp_dir: str, logger: UserLogger):
    allowed_coding_style_errors = ALLOWED_CODING_STYLE_ERRORS[:]

    # Barak wants a codingStyle check for long  functions that will not show up in presubmission, so we exclude it here.
    # Check is called readability-function-size
    # allowed_coding_style_errors += ["lines including whitespace and comments (threshold", "exceeds recommended size/complexity thresholds"]
    allowed_coding_style_errors += ["header guard does not follow preferred style"]
    require_codingstyle_check = ex_info.required_src_files + ex_info.required_hdr_files + ex_info.bonus_files
    coding_style_fails = ps_utils.check_folder_coding_style(temp_dir,
                                                            include_dir=ex_info.get_presubmit_or_test_include_dir(),
                                                            check_files=require_codingstyle_check,
                                                            exclude_msgs=allowed_coding_style_errors,
                                                            lang=ex_info.get_lang(),
                                                            disable_print=logger.disable_prints)
    for _type in coding_style_fails:
        num_fails = coding_style_fails[_type]
        logger.write_error_code(
            f"CodingStyleError_{_type[1:-1]}(max*{min(num_fails, 5)})"
            f"{{{num_fails} occurrences of this error.}}")
        for ign in IGNORE_CODINGSTYLE_ERRORS:
            if _type in ign or ign in _type:
                coding_style_fails[_type] = 0
    if coding_style_fails:
        fails_to_sum = [coding_style_fails[_type] for _type in coding_style_fails if _type[1:-1] not in NO_SUM_CODING_STYLE_ERRORS]
        num_fails = sum(fails_to_sum)
        logger.write_error_code(f"CodingStylePenalty_{min(num_fails, MAX_CODINGSTYLE_PENALTY)}")
        logger.write_debug(f"codingStyle errors\n: {coding_style_fails}\n")


def compile_code(ex_info: ExInfo, bonus_submitted: bool, executable_name: str, logger: UserLogger):
    logger.write_debug("Compilation check...")

    if ex_info.get_lang() == "C":
        # should we use -Werror ?
        compilation_cmds = [
            f"gcc -Wextra -Wall -Wvla -std=c99  -I . -I{ex_info.get_presubmit_or_test_include_dir()} "
            f"{' '.join(ex_info.required_src_files + ex_info.get_presubmit_srcs())}  -o {executable_name} -lm"]
    else:
        compilation_cmds = [
            f"g++ -g -Wextra -Wall -Wvla -std=c++20  -I . -I{ex_info.get_presubmit_or_test_include_dir()} "
            f"{' '.join(ex_info.required_src_files + ex_info.get_presubmit_srcs())}  -o {executable_name} -lm"]

    for symbol in ex_info.presubmit_compilation_wrap_symbols:
        compilation_cmds[0] += f" -Wl,--wrap={symbol}"

    may_have_warnings = False
    for compile_cmd in compilation_cmds:
        if bonus_submitted:
            compile_cmd += f" -D{ex_info.bonus_macro}"
        output_capture = [""]
        compile_result = ps_utils.compile(compile_cmd, capture_output=output_capture,
                                          disable_print=logger.disable_prints)
        if compile_result:
            logger.write_debug(PRESUBMIT_FAILED_MESSAGE)
            logger.write_error_code("COMPILATION_FAILED{Compilation failed.}")
            raise BadSubmissionException("Compilation failed.")
        if output_capture[0]:
            may_have_warnings = True
            logger.write_debug(f"Compilation warning: {output_capture[0]}")
            logger.write_error_code("TestWerror_compile")

    if may_have_warnings:
        logger.write_debug("""=============================================
You appear to have some compilation warnings.
Make sure to fix them for full marks!
=============================================\n""")
        logger.add_test_result(False)
    else:
        logger.write_debug("Compilation looks good!\n")


def run_ast_tests(ex_info: ExInfo, temp_dir: str, logger: UserLogger, test_numbers: List[int]):
    for ast_test_index in test_numbers:
        logger.write_debug("\n=====================")
        logger.write_debug(f"Running AST Test Number {ast_test_index}...")
        test_files_prefix = ex_info.get_autotests_src_dir() + f"/{AST_TESTS_PREFIX}{ast_test_index}"
        matches = ps_utils.checkASTMatches(temp_dir,
                                           src_files=ex_info.required_src_files + ex_info.presubmit_additional_srcs,
                                           matchers_file=f"{test_files_prefix}.match",
                                           include_dir=ex_info.get_presubmit_or_test_include_dir(),
                                           lang=ex_info.get_lang())
        required_matches = ps_utils.parseRequiredMatcehs(f"{test_files_prefix}.res")
        info = ps_utils.parseASTInfo(f"{test_files_prefix}.info")
        passed = False
        if required_matches is not None and required_matches == matches:
            passed = True
        elif required_matches is None and matches == 0:
            passed = True
        logger.add_test_result(passed)
        if passed:
            logger.write_debug("Passed Test.")
        else:
            logger.write_debug(f"Failed AST test. Info:\n{info}")
            logger.write_error_code(f"{AST_TESTS_ERRORCODE_PREFIX}{ast_test_index}")
        logger.write_debug("=====================\n")


def run_makefile_tests(ex_info: ExInfo, temp_dir: str, logger: UserLogger, makefile_tests: dict[str, List[str]],
                       ):
    for target in makefile_tests:
        logger.write_debug("\n=====================")
        logger.write_debug(f"Running Makefile target {target}...")
        make_dir = ps_utils.createTempDir('labcc_make_')
        os.chdir(make_dir)
        os.system(f"cp \"{temp_dir}\"/* \"{make_dir}\" > /dev/null 2> /dev/null")
        os.system(f"cp \"{ex_info.get_presubmit_or_test_include_dir()}\"/* \"{make_dir}\" > /dev/null 2> /dev/null")
        # os.system(f"cp {presubDir}/srcs/* {make_dir} > /dev/null 2> /dev/null")
        # TODO bshor: should this be get_presubmit_src_dir?
        os.system(f"cp \"{ex_info.get_autotests_src_dir()}\"/* \"{make_dir}\" > /dev/null 2> /dev/null")
        res = ps_utils.safeRunCMD(f"make {target}", MAX_SECS_TEST, print_output=not logger.disable_prints,
                                  disable_print=logger.disable_prints)
        if res:
            logger.write_debug("Make Error!")
            logger.write_error_code(f"{MAKEFILE_TESTS_ERRORCODE_PREFIX}{target}"
                                    f"{{makefile target execution raised an error!}}")
            logger.add_test_result(False)
        else:
            for filename in makefile_tests[target]:
                if not os.path.isfile(os.path.join(make_dir, filename)):
                    logger.write_debug(f"Missing required product of target {target}: {filename} !")
                    logger.add_test_result(False)
                    break
            else:
                logger.add_test_result(True)
                logger.write_debug('Success!')
        os.chdir(temp_dir)
        os.system(f"rm -rf {make_dir} > /dev/null 2> /dev/null")
        logger.write_debug("=====================\n")


def _compare_files(output_path: str, school_output_path: str, name: str, comparsion_script: str, test_info: str,
                   logger: UserLogger, error_code_prefix: str):
    if os.path.isfile(school_output_path):
        school_path_to_print = school_output_path
        if OVERRIDE_SCHOOL_OUTPUT_FOLDER:
            school_path_to_print = os.path.join(OVERRIDE_SCHOOL_OUTPUT_FOLDER, os.path.basename(school_output_path))
        test_info += f"\nto read school output, log into the school computers and enter the following command:" \
                     f"\ncat {school_path_to_print}\n"
        if not os.path.isfile(output_path):
            logger.write_debug(f"{name} file is missing!")
            logger.write_debug(f"Test Info: {test_info}")
            logger.write_debug("=====================\n")
            logger.write_error_code(f"{error_code_prefix}_diff"
                                    f"{{Your Program did not produce a required {name} file}}")
            return False
        # are_outputs_equal = open(output_path).read() == open(school_output_path).read()
        res = ps_utils.safeRunCMD(
            f"python3 {comparsion_script} {output_path} {school_output_path}",
            MAX_SECS_TEST, disable_print=True, timeout_code='timeout')
        if res:
            if res == "timeout":
                logger.write_debug("Failed with timeout!")
                logger.write_error_code(f"{error_code_prefix}_timeout"
                                        f"{{Your generated {name} caused a timeout}}")
            else:
                logger.write_debug("Failed with wrong output!")
                logger.write_debug("Your output:")
                ps_utils.print_output_file(output_path, no_print=logger.disable_prints)
                logger.write_error_code(f"{error_code_prefix}_diff"
                                        f"{{Your program produced the wrong {name}}}")

            logger.write_debug(f"Test Info: {test_info}")
            logger.write_debug("=====================\n")
            return False
    return True


def _parse_valgrind_results(temp_dir: str, val_result: ElementTree, error_code_prefix: str, logger: UserLogger):
    val_error_code = f"{error_code_prefix}_valgrind"
    if not val_result:
        logger.write_debug(f"No valgrind output found for {error_code_prefix}. This probably "
                           f"means valgrind died unexpectedly")
        logger.write_error_code(f"{val_error_code}{{Valgrind died while running your code.}}")
    else:
        val_xml_output_path = os.path.join(temp_dir, f"val_out{error_code_prefix}")
        val_result.write(val_xml_output_path)
        logger.debug([val_xml_output_path])
        root = val_result.getroot()
        for error in root:
            if error.tag == "error":
                kind = error.find('kind').text
                errorcode_kind = VALGRIND_TYPE_TO_ERRORCODE_DICT[kind]
                logger.add_valgrind_error(errorcode_kind)
                logger.write_error_code(val_error_code + f"{{valgrind error: {kind}}}")


def run_io_tests(ex_info: ExInfo, temp_dir: str, executable_name: str, logger: UserLogger, test_numbers: List[int],
                 should_use_valgrind: bool = False):
    for test_index in test_numbers:
        logger.write_debug("\n=====================")
        logger.write_debug(f"Running IO Test Number {test_index}")
        test_files_prefix = ex_info.get_autotests_src_dir() + f"/{IO_TESTS_PREFIX}{test_index}"

        _check_test_output(logger=logger,
                           test_files_prefix=test_files_prefix,
                           output_path_filename=f"{IO_STUDENT_OUTPUT_PATH_PREFIX}{test_index}",
                           error_code_prefix=f"{IO_TESTS_ERRORCODE_PREFIX}{test_index}",
                           executable_name=executable_name,
                           should_use_valgrind=should_use_valgrind,
                           temp_dir=temp_dir,
                           comparsion_script_path=ex_info.comparsion_script_path
                           )


def _check_run_command(test_cmd: str, temp_dir: str, logger: UserLogger, error_code_prefix: str, test_info: str,
                       expected_code: Optional[int] = None, should_use_valgrind: bool = False,
                       additional_params: Optional[dict] = None) -> bool:
    if additional_params is None:
        additional_params = {}

    val_result = None
    if should_use_valgrind:
        res, val_result = ps_utils.runValgrind(test_cmd, MAX_SECS_TEST, temp_dir, **additional_params)
    else:
        res = ps_utils.safeRunCMD(test_cmd, MAX_SECS_TEST, **additional_params, timeout_code="timeout",
                                  disable_print=logger.disable_prints)

    # I am not sure why is that here, not in presubmit, but yes in autotests
    if 128 - res in SEGFAULT_CODES:
        res = 128 - res

    if res in SEGFAULT_CODES:
        logger.write_debug(f"Failed With Segmentation fault! code={res}")
        logger.write_debug(f"Test Info: {test_info}")
        logger.write_debug("=====================\n")
        logger.add_test_result(False)
        logger.write_error_code(f"{error_code_prefix}_segfault"
                                f"{{your program crashed with: {SEGFAULT_CODES[res]}}}")
        logger.segfault_counter += 1
        return False

    if expected_code is not None and expected_code != res or res == "timeout":
        if res == "timeout":
            logger.write_debug("Failed with timeout!")
            logger.write_error_code(f"{error_code_prefix}_timeout")
        else:
            logger.write_debug(f"Failed with wrong exit code!\nExpected: {expected_code}, got: {res}.")
            logger.write_error_code(f"{error_code_prefix}_diff"
                                    f"{{Your Program exited with the wrong code.}}")
        logger.write_debug(f"Test Info: {test_info}")
        logger.add_test_result(False)
        logger.write_debug("=====================\n")
        return False

    if should_use_valgrind:
        _parse_valgrind_results(temp_dir, val_result, error_code_prefix, logger)

    return True

def _check_test_output(logger: UserLogger,
                       test_files_prefix: str,
                       output_path_filename: str,
                       error_code_prefix: str,
                       executable_name: str,
                       should_use_valgrind: bool,
                       temp_dir: str,
                       comparsion_script_path :str,
                       ):
    stdout_path = f"stu_stdout"
    stderr_path = f"stu_stderr"
    # this name is used in the TestIO_XX.args files
    output_path = output_path_filename

    school_output_path = f"{test_files_prefix}.out"
    school_stdout_path = f"{test_files_prefix}.stdout"
    school_stderr_path = f"{test_files_prefix}.stderr"

    args = ps_utils.parseArgs(f"{test_files_prefix}.arg")
    stdin = ps_utils.parseStdIn(f"{test_files_prefix}.stdin")
    code = ps_utils.parseCode(f"{test_files_prefix}.code")
    parsed_info = ps_utils.parseASTInfo(f"{test_files_prefix}.info")

    test_cmd = f"./{executable_name} {args}"

    os.system(f"cp {test_files_prefix}.in* . > /dev/null 2> /dev/null")

    extra_info = ""
    if parsed_info:
        extra_info = f"\nExtra info for test:\n{parsed_info}\n"
    test_info = f"\ntest command and arguments(\"{executable_name}\" is the name of the compiled program):" \
                f"\n" + test_cmd + "\n" + extra_info
    if stdin:
        school_path_to_print = test_files_prefix + ".stdin"
        if OVERRIDE_SCHOOL_OUTPUT_FOLDER:
            school_path_to_print = os.path.join(OVERRIDE_SCHOOL_OUTPUT_FOLDER, os.path.basename(school_path_to_print))
        test_info += f"\nto read test stdin, log into the school computers and enter the following command:" \
                     f"\ncat {school_path_to_print}\n"

    success = _check_run_command(test_cmd=test_cmd, logger=logger, error_code_prefix=error_code_prefix,
                                 test_info=test_info, temp_dir=temp_dir, expected_code=code,
                                 should_use_valgrind=should_use_valgrind, additional_params={"stdin": stdin,
                                                                                             "stdout_path": stdout_path,
                                                                                             "stderr_path": stderr_path})
    if not success:
        return
    compare_files_args = {
        "comparsion_script": comparsion_script_path,
        "test_info": test_info,
        "logger": logger,
        "error_code_prefix": error_code_prefix
    }

    if not (
            _compare_files(output_path, school_output_path, "output", **compare_files_args) and
            _compare_files(stdout_path, school_stdout_path, "stdout", **compare_files_args) and
            _compare_files(stderr_path, school_stderr_path, "stderr", **compare_files_args)
    ):
        logger.add_test_result(False)
        return

    logger.add_test_result(True)
    logger.write_debug("Passed Test.")
    logger.write_debug("=====================")


def run_comparsion_tests(ex_info: ExInfo, temp_dir: str,  logger: UserLogger, test_numbers: List[int],
                         should_use_valgrind: bool = False):
    if len(test_numbers) == 0:
        return

    # prepare compile params
    include_io_dir = ex_info.get_autotests_src_dir()
    base_compile = "gcc -Wextra -Wall -Wvla -std=c99" if ex_info.get_lang() == "C" \
        else "g++ -g -Wextra -Wall -Wvla -std=c++20"
    base_compile += f" -I . -I{ex_info.get_presubmit_or_test_include_dir()} -I{include_io_dir} -I{temp_dir}"
    lang_ext = 'c' if ex_info.get_lang() == "C" else 'cpp'
    os.system(f"cp \"{ex_info.get_presubmit_or_test_src_dir()}\"/* . > /dev/null 2> /dev/null")
    # TODO bshor: previously they removed the last file in the additional list, but I don't see why
    src_files = ex_info.required_src_files + ex_info.presubmit_additional_srcs

    logger.write_debug("Running Comparison Tests")
    logger.write_debug("in this section, we will compile your code with additional files and run comparison tests\n")
    for test_index in test_numbers:
        logger.write_debug("=====================")
        logger.write_debug(f"Testing Comparison Test {test_index}")
        error_code_prefix = f"{COMPARISON_TESTS_ERRORCODE_PREFIX}{test_index}"

        prog_name = f"test_{test_index}"
        compile_cmd = f"{base_compile} {include_io_dir}/{COMPARISON_TESTS_PREFIX}{test_index}.{lang_ext} " \
                      f"{' '.join(src_files)} -o {prog_name}"
        res = ps_utils.compile(compile_cmd)
        if res != 0:
            logger.write_debug(f"Failed to compile comparison test {test_index}")
            logger.write_debug("Test info:")
            logger.write_debug("compile command: ")
            logger.write_debug(compile_cmd)
            logger.write_debug("=====================")
            logger.write_error_code(f"{error_code_prefix}_compile")
            logger.add_test_result(False)
            continue

        test_files_prefix = ex_info.get_autotests_src_dir() + f"/{COMPARISON_TESTS_PREFIX}{test_index}"

        _check_test_output(logger=logger,
                           test_files_prefix=test_files_prefix,
                           output_path_filename=f"{COMPARISON_STUDENT_OUTPUT_PATH_PREFIX}{test_index}",
                           error_code_prefix=error_code_prefix,
                           executable_name=prog_name,
                           should_use_valgrind=should_use_valgrind,
                           temp_dir=temp_dir,
                           comparsion_script_path=ex_info.comparsion_script_path
                           )


def _run_comp_tests(ex_info: ExInfo, temp_dir: str, logger: UserLogger, is_positive: bool, tests_indexes: List[int]):
    if len(tests_indexes) == 0:
        return

    label = "Positive" if is_positive else "Negative"
    test_prefix = P_COMPILATION_TESTS_PREFIX if is_positive else N_COMPILATION_TESTS_PREFIX

    include_io_dir = ex_info.get_autotests_src_dir()
    base_compile = "gcc -Wextra -Wall -Wvla -std=c99" \
        if ex_info.get_lang() == "C" else "g++ -g -Wextra -Wall -Wvla -std=c++20"
    base_compile += f" -I . -I{ex_info.get_presubmit_or_test_include_dir()} -I{include_io_dir} -I{temp_dir}"
    lang_ext = 'c' if ex_info.get_lang() == "C" else 'cpp'
    # TODO bshor: previously they removed the last file in the additional list, but I don't see why
    src_files = ex_info.required_src_files + ex_info.presubmit_additional_srcs

    logger.write_debug(f"Running {label} Compilation Tests")
    logger.write_debug("in this section, we will compile your code with additional files and check that it compiles successfully\n")
    for test_index in tests_indexes:
        logger.write_debug("=====================")
        logger.write_debug(f"Testing {label} Compilation Test {test_index}")
        prog_name = f"test_{test_index}"
        compile_cmd = f"{base_compile} {include_io_dir}/{test_prefix}{test_index}.{lang_ext} " \
                      f"{' '.join(src_files)} -o {temp_dir}/{prog_name}"
        res = ps_utils.compile(compile_cmd)
        if (is_positive and res != 0) or (not is_positive and res == 0):
            logger.write_debug(f"failed on {label} compilation test {test_index} {res}")
            logger.write_debug("Test info:")
            logger.write_debug("compile command: ")
            logger.write_debug(compile_cmd)
            logger.write_debug("=====================")
            logger.write_error_code(f"{test_prefix}{test_index}_compile")
            logger.add_test_result(False)
            continue
        logger.add_test_result(True)
        logger.write_debug(f"Passed {label} Compilation Test {test_index}")
        logger.write_debug("=====================\n")


def run_pcomp_tests(ex_info: ExInfo, temp_dir: str, logger: UserLogger, test_indexes: List[int]):
    return _run_comp_tests(ex_info, temp_dir, logger, True, test_indexes)


def run_ncomp_tests(ex_info: ExInfo, temp_dir: str, logger: UserLogger, test_indexes: List[int]):
    return _run_comp_tests(ex_info, temp_dir, logger, False, test_indexes)


def run_unit_tests(ex_info: ExInfo, temp_dir: str, logger: UserLogger, test_indexes: List[int],
                   should_use_valgrind: bool = False):
    if len(test_indexes) == 0:
        return

    include_dir = ex_info.get_autotests_src_dir()
    base_compile = "gcc -Wextra -Wall -Wvla -std=c99" \
        if ex_info.get_lang() == "C" else "g++ -g -Wextra -Wall -Wvla -std=c++20"
    base_compile += f" -I . -I{ex_info.get_presubmit_or_test_include_dir()} -I{include_dir} -I{temp_dir}"
    lang_ext = 'c' if ex_info.get_lang() == "C" else 'cpp'
    # TODO bshor: previously they removed the last file in the additional list, but I don't see why
    src_files = ex_info.required_src_files + ex_info.presubmit_additional_srcs

    logger.write_debug("Running Unit Tests")
    logger.write_debug("in this section, we will compile your code with additional files and run some unit tests\n")
    for unit_test_index in test_indexes:
        error_code_prefix = f"{UNIT_TESTS_ERRORCODES_PREFIX}{unit_test_index}"

        logger.write_debug("=====================")
        logger.write_debug(f"Testing Unit Test {unit_test_index}")
        prog_name = f"test_{unit_test_index}"
        compile_cmd = f"{base_compile} {include_dir}/{UNIT_TESTS_PREFIX}{unit_test_index}.{lang_ext} " \
                      f"{' '.join(src_files)} -o {prog_name}"
        res = ps_utils.compile(compile_cmd)
        if res != 0:
            logger.write_debug(f"failed to compile unit test {unit_test_index}")
            logger.write_debug("Test info:")
            logger.write_debug("compile command: ")
            logger.write_debug(compile_cmd)
            logger.write_debug("=====================")
            logger.write_error_code(f"{error_code_prefix}_compile")
            logger.add_test_result(False)
            continue
        test_cmd = f"./{prog_name}"

        success = _check_run_command(test_cmd=test_cmd, logger=logger, error_code_prefix=error_code_prefix, test_info="",
                                     temp_dir=temp_dir, should_use_valgrind=should_use_valgrind)
        if not success:
            continue

        logger.add_test_result(True)
        logger.write_debug(f"Passed Unit Test {unit_test_index}")
        logger.write_debug("=====================\n")


def run_presubmit_tests(ex_info: ExInfo, temp_dir: str, logger: UserLogger, executable_name: str):
    # run the presubmit{.c,.cpp} file
    logger.write_debug("=====================")
    logger.write_debug("Presubmit Test")

    test_cmd = f"./{executable_name}"
    os.system(
        f"cp {ex_info.get_presub_src_dir()}/{PRESUBMIT_INPUTS_PREFIX_FORMAT}* . > /dev/null 2> /dev/null")

    all_test_results = []
    success = _check_run_command(test_cmd=test_cmd, logger=logger, temp_dir=temp_dir, test_info="",
                                 error_code_prefix=PRESUBMISSION_TESTS_ERRORCODE_PREFIX)

    if not success:
        return
    logger.add_test_result(True)

    logger.write_debug("Test Passed!")
    logger.write_debug("=====================\n")
    return all_test_results