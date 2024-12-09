"""
This file contains some constants required for the info file. You may ignore it.
"""
import os
from enum import Enum


class STUDENT_OUTPUT(Enum):
	FILE = 1
	STDOUT = 2


DIR_PRESUB_SRC = "presubmit_src"
DIR_PRESUB_HDR = "presubmit_headers"
DIR_SCHOOL_SOL = "school_solution"
DIR_AUTOTESTS_SRC = "autotest_src"
DIR_AUTOTESTS_HDR = "autotest_headers"
DIR_ERRORCODES = "errorcodes"

IO_TESTS_PREFIX = "TestIO_"
UNIT_TESTS_PREFIX = "Test_"
COMPARISON_TESTS_PREFIX = "TestComparison_"
BONUS_TESTS_PREFIX = "TestBonus_"
P_COMPILATION_TESTS_PREFIX = "TestPCompilation_"
N_COMPILATION_TESTS_PREFIX = "TestNCompilation_"
AST_TESTS_PREFIX = "TestAST_"
