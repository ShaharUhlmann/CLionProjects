IO_TESTS_PREFIX = "TestIO_"
UNIT_TESTS_PREFIX = "Test_"
COMPARISON_TESTS_PREFIX = "TestComparison_"
BONUS_TESTS_PREFIX = "TestBonus_"
P_COMPILATION_TESTS_PREFIX = "TestPCompilation_"
N_COMPILATION_TESTS_PREFIX = "TestNCompilation_"
AST_TESTS_PREFIX = "TestAST_"

IO_STUDENT_OUTPUT_PATH_PREFIX = "TestIO_out_"
COMPARISON_STUDENT_OUTPUT_PATH_PREFIX = "TestComparison_out_"

PRESUBMIT_INPUTS_PREFIX_FORMAT = "presubmit.in"

IO_TESTS_ERRORCODE_PREFIX = "TestIO_"
AST_TESTS_ERRORCODE_PREFIX = "TestAST_"
MAKEFILE_TESTS_ERRORCODE_PREFIX = "TestMakefile_"
UNIT_TESTS_ERRORCODES_PREFIX = "Test_"
COMPARISON_TESTS_ERRORCODE_PREFIX = "TestComparison_"

# currently not used
PRESUBMISSION_TESTS_ERRORCODE_PREFIX = "TestComparison_"
# DATE_TESTS_ERRORCODE_PREFIX = "EarlySubmissionDays_"


SEGFAULT_CODES = {-11: "Signal 11 Segmentation Fault",
                  -6: "Signal 6 Abort - most likely failed assert or uncaught exception",
                  -8: "Signal 8 Floating Point Error - most likely division by zero",
                  -4: "Signal 4 Illegal Instruction - most likely use of a faulty function pointer"}

ALLOWED_CODING_STYLE_ERRORS = ["has cognitive complexity of",
                               "unknown type name",
                               "header guard does not follow preferred style"]

MAX_SECS_TEST = 60


IGNORE_CODINGSTYLE_ERRORS = ["readability-magic-numbers"]
NO_SUM_CODING_STYLE_ERRORS = ["readability-function-size"]
MAX_CODINGSTYLE_PENALTY = 10


VALGRIND_TYPE_TO_ERRORCODE_DICT = {
    "UninitCondition": "uninitialised_values",
    "UninitValue": "uninitialised_values",
    "SyscallParam": "uninitialised_values",
    "Leak_DefinitelyLost": "memory_leaks",
    "InvalidFree": "memory_leaks",
    "InvalidRead": "invalid_read/write",
    "InvalidWrite": "invalid_read/write",
    "InvalidJump": "segmentation_faults",
    "MismatchedFree": "memory_leaks",
    "Leak_PossiblyLost": "memory_leaks",
    "Overlap": "invalid_read/write",
    "FishyValue": "invalid_read/write",
    'Leak_StillReachable': "memory_leaks",
    'Leak_IndirectlyLost': "memory_leaks"
}

MAX_VALGRIND_ERRORCODE_MAX_COUNT = {
    "uninitialised_values": 15,
    "memory_leaks": 10,
    "invalid_read/write": 14,
    "segmentation_faults": 0
}

PRESUBMIT_FAILED_MESSAGE = """*****************************************
*                  !!!                  *
* Presubmission Script Failed Entirely! *
*                                       *
*  You must fix the problems, otherwise *
*   this submission's grade will be 0!  *
*                  !!!                  *
*****************************************
"""
