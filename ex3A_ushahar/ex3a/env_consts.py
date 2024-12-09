import os
import shutil

this_file_path = os.path.dirname(os.path.realpath(__file__))
resources_path = os.path.join(this_file_path, 'resources')
CLANG_TIDY_PATH = shutil.which("clang-tidy")
# assert CLANG_TIDY_PATH is not None, "clang-tidy not found in PATH"
CLANG_QUERY_PATH = shutil.which("clang-query")
# assert CLANG_QUERY_PATH is not None, "clang-query not found in PATH"

if CLANG_TIDY_PATH is None:
    CLANG_TIDY_PATH = '/cs/course/2023/labcc2/bin/clang-tidy'
    CLANG_QUERY_PATH = '/cs/course/2023/labcc2/bin/clang-query'
if not os.path.exists(CLANG_TIDY_PATH):
    CLANG_TIDY_PATH = CLANG_QUERY_PATH = None
    
CLANG_TIDY_CONFIG = os.path.join(resources_path, 'clang_tidy_conf')
CLANG_TIDY_TO_JUNIT_PATH = os.path.join(resources_path, 'clang_tidy_to_junit.py')
OVERRIDE_SCHOOL_OUTPUT_FOLDER = None
