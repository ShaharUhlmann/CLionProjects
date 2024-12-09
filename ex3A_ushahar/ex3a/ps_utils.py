import fnmatch
import re
import shlex
import tempfile
# import popen2
import subprocess
import time
import resource
import signal
import os
import atexit
# import sets
import sys
import hashlib
import xml.etree.ElementTree as ET
from env_consts import CLANG_TIDY_PATH, CLANG_TIDY_TO_JUNIT_PATH, CLANG_TIDY_CONFIG, CLANG_QUERY_PATH


# courseDir = "/cs/course/current/labcc2"
# binDir = f"{courseDir}/bin"


# generate MD5 Checksum for a file
def md5checksum(file):
    with open(file, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def check_file_coding_style(file, fails=None, include_dir="", exclude_msgs=None, lang='C', line_length=79,
                            disable_print=False):
    if fails is None:
        fails = dict()
    path = os.path.abspath(file + '/..')

    outputFile = f"{path}/temp_out"
    cl_tdy_cmd = f"{CLANG_TIDY_PATH} --quiet"
    convert_cmd = CLANG_TIDY_TO_JUNIT_PATH
    include_dir_flag = f"-- -I{include_dir}" if include_dir else "-- "
    if lang == 'C++':
        include_dir_flag += f" -std=c++20 -x c++ -isystem/usr/lib/gcc/x86_64-linux-gnu/10/include"
    elif lang == 'C':
        include_dir_flag += f" -std=c99 -isystem/usr/lib/gcc/x86_64-linux-gnu/10/include"
    # print("Running", f"{cl_tdy_cmd} {file} {include_dir_flag} 2> /dev/null | {convert_cmd} {path} > {outputFile} ")
    # print("clang-tidy output0", os.system(f"{cl_tdy_cmd} {file} {include_dir_flag} > {outputFile}"))
    # print("clang-tidy output0", open(outputFile).read())

    os.system(f"{cl_tdy_cmd} {file} {include_dir_flag} 2> /dev/null | {convert_cmd} {path} > {outputFile} ")

    # print("clang-tidy output", open(outputFile).read())

    result = ET.parse(outputFile)
    os.system(f"rm -f {outputFile} 2> /dev/null > /dev/null")
    root = result.getroot()
    for suite in [suite for suite in root if file.endswith(suite.attrib['name'][1:])]:
        for case in suite:
            for failure in case:
                msg = failure.attrib['message']
                attr = case.attrib['id'].replace('/', ':').split()
                loc = attr[0]
                _type = attr[1]
                content = failure.text
                for excl in exclude_msgs:
                    if msg.find(excl) > -1:
                        break
                else:
                    if not disable_print:
                        print(f"Problem: in {file}, line {loc}, {msg}\n{content}")
                    fails[_type] = 1 if _type not in fails else fails[_type] + 1
    with open(file, 'r') as f:
        lines = f.read().split('\n')
    lens = [len(line) for line in lines]
    max_len = max(lens)
    if max_len > line_length:
        if not disable_print:
            print(
                f"Problem: in {file}, line {lens.index(max_len) + 1} is longer than {line_length} characters and will"
                f" be truncated.")
    return fails


def check_folder_coding_style(path, include_dir="", check_files=None, exclude_msgs=None, lang='C', disable_print=False,
                     typedefs=None):
    if typedefs is None:
        typedefs = []
    if exclude_msgs is None:
        exclude_msgs = set()
    if check_files is None:
        check_files = []
    if not disable_print:
        print("Checking CodingStyle...")
    fails = dict()
    os.system(f"cp {CLANG_TIDY_CONFIG} {path}")  # > /dev/null 2> /dev/null")

    for filename in check_files:
        if not disable_print:
            print(f"Checking file {filename}...")
        if filename.endswith('.c') or filename.endswith('.cpp') or filename in check_files:
            fails.update(check_file_coding_style(filename, fails, include_dir, exclude_msgs, lang,
                                                 disable_print=disable_print))
    if not fails:
        if not disable_print:
            print("Passed codingStyle check.")
    os.system(f"rm -f {path}/.clang-tidy")
    return fails

def checkASTFucntionUsageExists(dir, src_files, include_dir, function_name, lang='C'):
    matchers_file = f"{dir}/.temp_matcher"
    with open(matchers_file, 'w') as f:
        f.write(f'm callExpr(callee(functionDecl(hasName("{function_name}"))), '
                f'isExpansionInMainFile())\n')
    return checkASTMatches(dir, src_files, matchers_file, include_dir, lang) != 0


def checkASTMatches(dir, src_files, matchers_file, include_dir, lang='C'):
    cl_query = CLANG_QUERY_PATH
    include_dir_flag = f"--extra-arg=-I{include_dir} --extra-arg=-I." if include_dir else ""
    output_file = ".astOut"
    reg = re.compile('[^\\d]*(\\d+) (match|matches)\\.')
    total_matches = 0
    if lang == 'C++':
        include_dir_flag += f" --extra-arg=-x --extra-arg=c++ --extra-arg=-I/usr/lib/llvm-11/lib/clang/11.0.1/include/"
        # include_dir_flag += f" --extra-arg=-x --extra-arg=c++"
    elif lang == 'C':
        include_dir_flag += f" --extra-arg=-I/usr/lib/llvm-11/lib/clang/11.0.1/include/"
    for file in src_files:
        if not os.path.isfile(file):
            file = os.path.join(dir, file)
        os.system(
            f"{cl_query} -f={matchers_file} {include_dir_flag} {file} 2> /dev/null > {output_file} ")
        # print("running query", f"{cl_query} -f={matchers_file} {include_dir_flag} {file} 2> /dev/null > {output_file} ")
        # print("output", os.system(f"{cl_query} -f={matchers_file} {include_dir_flag} {file}"))
        # print("output_matchers", open(matchers_file).read())
        with open(output_file, 'r') as f:
            result = f.read()
        os.remove(output_file)
        if result:
            search_res = re.search(r'[^\d]*(\d+) (match|matches)\.', result)
            num_matches = search_res.groups()[0]
            total_matches += int(num_matches)
            # print("Found", num_matches, "matches in", file, "for", open(matchers_file, "r").read(), result,
            #       f"{cl_query} -f={matchers_file} {include_dir_flag} {file}")
    return total_matches


def checkPragmas(path):
    for root, dir, fs in os.walk(path):
        for filename in fs:
            with open(os.path.join(root, filename), 'r', errors='replace') as f:
                content = f.read()
            for match in re.finditer("#\\w*pragma", content):
                return filename
    return None


# check to see if any files are empty.
def emptyFiles(path, disable_print=False):
    # get list of all files. including subdirectories.
    if not disable_print:
        print("Making sure files are not empty...")
    found = False
    for root, dir, files in os.walk(path):
        for fileName in files:
            if not os.path.getsize(os.path.join(root, fileName)):
                if not disable_print:
                    print("\t empty file found:", fileName)
                found = True
    if found:
        return 1
    else:
        if not disable_print:
            print("OK")
        return 0


# Open the given file in the current directory.
def extractTar(tarFile, disable_print=False):
    if not disable_print:
        print("Opening tar file", tarFile)
    # expand the tar file into a temp sub directory.
    if not os.path.exists(tarFile):
        if not disable_print:
            print("Could not find the file " + tarFile)
        return 1

    fd = subprocess.run(f'tar -xvf "{tarFile}" > /dev/null 2> /dev/null', shell=True).returncode
    if fd:
        tarName = os.path.split(tarFile)[1]
        if not disable_print:
            print("The file " + tarName + " is empty or is not a tar file.")
        return 2
    if not disable_print:
        print("OK")
    return 0


def print_output_file(filename, no_print=False):
    with open(filename, errors='surrogateescape') as f:
        if no_print:
            return f.read()
        print(f.read())


def parseRequiredMatcehs(filename):
    return parseCode(filename)


def parseASTInfo(filename):
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            return f.read()
    return ""


def parseCode(filename):
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            return int(f.read())
    return None


def parseStdIn(filename):
    if os.path.isfile(filename):
        with open(filename, 'rb') as f:
            return f.read()
    return ""


def parseArgs(filename):
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            return f.read()
    return ""


# a function used to recursively delete the given directory.
def cleanup(cleanDir):
    os.system("rm -rf " + cleanDir)


# create and return a temporary directory
def createTempDir(prefix):
    tempDir = tempfile.mkdtemp("", prefix)
    atexit.register(cleanup, tempDir)
    return tempDir


# brings files (recursively) from a given directory into the current dir.
def getFilesFrom(srcDir, to_print=True, overwrite=False):
    print("Importing files")
    if (overwrite):  # Don't ovewrite existing files
        cp_opt = ' -n '
    else:
        cp_opt = ''
    if not os.path.exists(srcDir):
        sys.stderr.write("can't find source directory " + srcDir + "\n")
        return 1
    elif os.system(f"cp -r {cp_opt} \"{srcDir}\"/* ."):
        sys.stderr.write("error when copying files from " + srcDir)
        return 2
    else:
        print("OK")
        if (to_print):
            print("imported from dir: " + srcDir)
            os.system("pwd")
            print("now content:")
            os.system("ls")
        return 0


# try to compile in the current directory
def compile(compileCmd, disable_print=False, capture_output=None):
    if not disable_print:
        print("Compiling...", compileCmd)
    compileResult = subprocess.run(args=compileCmd.split(), encoding='utf-8', stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
    if not disable_print:
        print(compileResult.stdout)
        if compileResult.returncode != 0:
            print("Compilation failed!")
    elif not disable_print:
        print("OK")
    if capture_output:
        capture_output[0] = compileResult.stdout
    return compileResult.returncode


def runValgrind(cmd, secs, tempDir=os.getcwd(), disable_print=True, stdin="", stdout_path="", stderr_path="",
                timeout_code=None):
    xml_file = f"{tempDir}/val_out"
    res = safeRunCMD(
        f"valgrind -q --xml=yes --xml-file={xml_file} --track-origins=yes --leak-check=full --show-leak-kinds=all {cmd}",
        secs, disable_print=disable_print, timeout_code=timeout_code, stdin=stdin, stdout_path=stdout_path,
        stderr_path=stderr_path)
    try:
        result = ET.parse(xml_file)
        os.system(f"rm -f {xml_file}")
    except ET.ParseError:
        result = None
    return res, result


##################################################################
#
#  run the given command for at most the given number of secs.
#      give some message in case of a crash.
#
##################################################################
def safeRunCMD(cmd, secs, stdin="", stdout_path="", stderr_path="", toPrint=False, disable_print=False,
               timeout_code=None, print_output=False):
    if not disable_print:
        print("Running test...")
    if (toPrint):
        print(cmd)
    # Set a cpu time limit.
    # The second secs was -1, but students complained that this row raise the next Err:
    # ValueError: not allowed to raise maximum limit
    # resource.setrlimit(resource.RLIMIT_CPU,(secs,-1))
    # resource.setrlimit(resource.RLIMIT_CPU,(30,30))
    # run the process.
    # res = os.system(cmd)
    # if stdout_path:
    #     cmd += f" > {stdout_path}"
    # if stderr_path:
    #     cmd += f" 2> {stderr_path}"
    try:
        proc = subprocess.run(shlex.split(cmd), capture_output=True, timeout=secs, input=stdin)

        # print("runoutput", proc.returncode, proc.stdout, proc.stderr, shlex.split(cmd))
        res = proc.returncode
        if stdout_path:
            with open(stdout_path, 'w') as sout:
                sout.write(proc.stdout.decode(errors='replace'))
        if stderr_path:
            with open(stderr_path, 'w') as serr:
                serr.write(proc.stderr.decode(errors='replace'))
        if print_output:
            print(proc.stdout.decode(errors='replace'))
            print(proc.stderr.decode(errors='replace'))
    except subprocess.TimeoutExpired as e:
        if not disable_print:
            print("Timeout occurred!")
        if timeout_code:
            return timeout_code
        else:
            raise e
    # lift the cpu time limit. (we don't need it)
    # Students complains that this row raise ValueError: not allowed to raise maximum limit
    # resource.setrlimit(resource.RLIMIT_CPU,(-1,-1))
    # detect the problem through the return value! :-)
    badlist = [signal.SIGBUS, signal.SIGFPE, signal.SIGSEGV, signal.SIGXFSZ]
    if not disable_print and res == signal.SIGXCPU or res - 128 == signal.SIGXCPU:
        print("exceeded cpu usage! We may have an endless loop!")
    elif not disable_print and res in badlist or res - 128 in badlist:
        print("Program Crashed!")
    elif res:
        pass
    # print "Test Failed"
    else:
        if not disable_print:
            print("OK")
    return res


##################################################################
#
#  Return a list of files from this list that were found.
#
##################################################################
def existingFiles(path, fileList):
    """ Return a list of files from this list that were found.
    """
    return list(filter(lambda x: os.path.exists(os.path.join(path, x)), fileList))


##################################################################
#
#  Return a list of files from the given list that are missing.
#
##################################################################
def missingFiles(path, fileList):
    """ Return a list of files from the given list that are missing.
    """
    return list(filter(lambda x: not os.path.exists(os.path.join(path, x)), fileList))


##################################################################
#
#  Check that the files in the given path match good patterns and
#      don't match bad ones.
#
##################################################################
def checkFiles(path, requiredFiles, notPermitedFiles, goodPatterns, badPatterns, disable_print=False):
    """ Make sure all required files are found in path, all nonPermited ones
    are missing, And that all files match some goodPattern and do not match any
    badPattern."""
    if not disable_print:
        print("Checking files...")
    # Look for required files. All of these must be present.
    missing = missingFiles(path, requiredFiles)

    # Look for any non permited files. All of these must be missing.
    notPermited = existingFiles(path, notPermitedFiles)

    # print results for both the searches:
    if missing:
        if not disable_print:
            print('Missing required files:')
        for name in missing:
            if not disable_print:
                print('\t', name)
    if notPermited:
        if not disable_print:
            print('Found excess files:')
        for name in notPermited:
            if not disable_print:
                print('\t', name)

    if missing or notPermited:
        return 1

    # get list of all files. including subdirectories.
    fileList = []
    for root, dir, files in os.walk(path):
        fileList.extend(files)
    # check for good Patterns. Every file must match one of these.
    notGood = fileList
    for pattern in goodPatterns:
        notGood = list(filter(lambda file: not fnmatch.fnmatchcase(file, pattern), notGood))

    if notGood:
        if not disable_print:
            print("Found unallowed files (no good pattern):")
        for file in notGood:
            if not disable_print:
                print('\t', file)
        return 1

    # check for bad Patterns. No file should match any of these.
    bigList = []
    for pattern in badPatterns:
        bigList.extend(filter(lambda file: fnmatch.fnmatchcase(file, pattern), fileList))

    if bigList:
        if not disable_print:
            print("Found unallowed files (bad pattern):")
            for file in set(bigList):
                print('\t', file)
        return 1
    if not disable_print:
        print("OK")
    return 0  # all is well that ends well!
