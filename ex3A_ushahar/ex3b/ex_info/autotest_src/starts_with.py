import sys
import re

# Both files (stdout and expected) starts with same values
BOTH_START_WITH = {
    15, 16, 17, 18, 19, 20, 21, 22
}

# Both files (stdout and expected) are equal
BOTH_EQUAL = {
    1,2,3,4,5,6,7,8,9,10,11,12,13,14,23
}

# Both files (TestIO_{key}.stdout and TestIO_{value}.stdout) are equal
SHOULD_BE_SAME = {

}

# Both files (TestIO_{key}.stdout and TestIO_{value}.stdout) are different
SHOULD_BE_DIFFERENT = {

}

# Check if in test {key} the string {value[0]} is in student stdout between {value[1]} and {value[2]} times
PROBABILITY_RANGE = {
    # Unified probability
    #16: ["x c.", 17, 32],
    #19: ["a b.", 25, 41],

    # Weighted probability
    #15: ["a a a a a a a a a a a a a a a a a a a a", 42, 50],
    #17: ["a x c.", 0, 8],
    #18: ["a x.", 0, 8]
}


def get_text_from_file(file_path):
    with open(file_path) as file:
        return file.read().replace(' \n', '\n').strip()


def get_student_file_path(test_num):
    return f'stu_stdout{test_num}'


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 diff.py <file1> <file2>")

    try:
        student_path = sys.argv[1]
        test_path = sys.argv[2]
        exit_code = False

        # Get test number from file name
        regex = re.compile(r'\d+')
        test_num = int(regex.findall(test_path)[-1])

        # Read school expected file and student submission stdout
        test_text = get_text_from_file(test_path)
        student_text = get_text_from_file(student_path)

        # From here logic is FLIPPED in exit_code!  (0 == False) pass test and (1 == True) fail test

        # Both files (stdout and expected) starts with same values
        if test_num in BOTH_START_WITH:
            exit_code = (not student_text.startswith(test_text)) or exit_code

        # Both files (stdout and expected) are equal
        if test_num in BOTH_EQUAL:
            exit_code = (not (test_text == student_text)) or exit_code

        # Both files (TestIO_{key}.stdout and TestIO_{value}.stdout) are equal
        if test_num in SHOULD_BE_SAME:
            # First check with school file
            if student_text.startswith(test_text):
                # If pass load and check with old result
                prev_test = SHOULD_BE_SAME[test_num]
                prev_test_path = get_student_file_path(prev_test)
                prev_student_text = get_text_from_file(prev_test_path)

                exit_code = (not (prev_student_text == student_text)) or exit_code
            else:  # Else return error
                exit_code = True

        # Both files (TestIO_{key}.stdout and TestIO_{value}.stdout) are different
        if test_num in SHOULD_BE_DIFFERENT:
            # First check with school file
            if student_text.startswith(test_text):
                # If pass load and check with old result
                prev_test = SHOULD_BE_DIFFERENT[test_num]
                prev_test_path = get_student_file_path(prev_test)
                prev_student_text = get_text_from_file(prev_test_path)

                exit_code = (not (prev_student_text != student_text)) or exit_code
            else:  # Else return error
                exit_code = True

        # Check if in the {key} the string {value[0]} is in the text between {value[1]} and {value[2]} times
        if test_num in PROBABILITY_RANGE:
            # Convert output to list of lines
            student_text_list = student_text.splitlines()

            # check if got exactly 50 lines
            if len(student_text_list) == 50:
                # Remove the string: "Tweet {i}: " from each line
                # If 1 < i < 10 it will always be the first 9 chars
                # If i >= 10 we will have space as first char (the 9'th char will be ':' now, instead of space).
                # .strip() will remove it
                student_text_list = [line[9:].strip() for line in student_text_list]

                # Count how many of them equal to given string
                expected_line, min_range, max_range = PROBABILITY_RANGE[test_num]
                count = student_text_list.count(expected_line)
                print(f'counter: {count}')

                exit_code = (not (min_range <= count <= max_range)) or exit_code
            else:
                exit_code = True

        sys.exit(exit_code)

    except FileNotFoundError:
        print("At least one of the given files was not found.")
        sys.exit(1)