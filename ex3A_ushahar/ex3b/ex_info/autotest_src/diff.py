import filecmp
import sys

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Usage: python3 diff.py <file1> <file2>")
	try:
		if filecmp.cmp(sys.argv[1], sys.argv[2], shallow=False):
			exit(0)
		exit(1)
	except FileNotFoundError:
		print("At least one of the given files was not found.")
		exit(1)
