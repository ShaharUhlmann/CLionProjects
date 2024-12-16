#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sort_bus_lines.h"
#include "test_bus_lines.h"

// Error messages
#define ARNM_ER "Usage: only a single argument is accepted"
#define AR_ER "Usage: allowed args: test/by_distance/by_duration/by_name"
#define NC_ER "Error: bus name should contains only digits and small chars"
#define D_ER "Error: distance should be "\
	"an integer between 0 and 1000 (includes)"
#define DU_ER "Error: duration should be "\
	"an integer between 10 and 100 (includes)"
#define LN_ER "Error: Number of lines should be a positive integer"

// Input messages
#define INPUT_MSG "Enter number of lines. Then enter\n"
#define INPUT_MSG2 "Enter line info. Then enter\n"

// Allowed characters
#define ALLOWED_CHARS "abcdefghijklmnopqrstuvwxyz0123456789"

// Argument indices
#define ARGUMENT 1
#define SINGLE_ARGUMENT 2

// Action types
#define BUBBLESORT 1
#define QUICKSORT 2
#define TEST 3

// Function declarations
int run_program(int action, SortType sort_type);

int string_to_int(const char *str, int *result);

int main(const int argc, char *argv[])
{
	if (argc == SINGLE_ARGUMENT)
	{ // Check if the argument is single and valid
		if (strcmp(argv[ARGUMENT], "by_distance") == 0)
		{
			return run_program(QUICKSORT, DISTANCE);
		}
		if (strcmp(argv[ARGUMENT], "by_duration") == 0)
		{
			return run_program(QUICKSORT, DURATION);
		}
		if (strcmp(argv[ARGUMENT], "by_name") == 0)
		{
			return run_program(BUBBLESORT, DURATION);
		}
		if (strcmp(argv[ARGUMENT], "test") == 0)
		{
			return run_program(TEST, DURATION);
		}
		fprintf(stdout, AR_ER);
	}
	else
	{
		fprintf(stdout, ARNM_ER);
	}
	return EXIT_FAILURE;
}

/**
 * Run the program according to the action and sort type
 *
 * @param action which action to perform, bubble sort, quick sort or test
 * @param sort_type default is DURATION, can be changed to DISTANCE
 * @return EXIT_SUCCESS if the ran successfully, EXIT_FAILURE otherwise
 */
int run_program(const int action, const SortType sort_type)
{
	int lines_num;
	char input[10];

	// Get the number of lines
	while (true)
	{
		printf("%s", INPUT_MSG);
		fgets(input, sizeof(input), stdin);
		if (string_to_int(input, &lines_num))
		{
			if (lines_num > 0)
			{
				break;
			}
		}
		printf("%s\n", LN_ER);
	}

	BusLine *line_arr = malloc(sizeof(BusLine) * lines_num);

	// Check if the allocation was successful
	if (line_arr == NULL)
	{
		return EXIT_FAILURE;
	}

	// Get the lines info, validate and store them
	for (int i = 0; i < lines_num; i++)
	{
		printf("%s", INPUT_MSG2);
		char line_input[60];
		fgets(line_input, sizeof(line_input), stdin);
		//check input has exactly 2 commas
		if (strchr(line_input, ',') == NULL
			|| strchr(strchr(line_input, ',') + 1, ',') == NULL)
		{
			printf("%s\n", NC_ER);
			i--;
			continue;
		}
		const char *name = strtok(line_input, ",");
		const char *distance_str = strtok(NULL, ",");
		const char *duration_str = strtok(NULL, ",");

		// Validate the name
		if (strspn(name, ALLOWED_CHARS) != strlen(name))
		{
			printf("%s\n", NC_ER);
			i--;
			continue;
		}

		int distance, duration;

		// Validate the distance and duration
		if (!string_to_int(distance_str, &distance)
			|| distance < 0
			|| distance > 1000)
		{
			printf("%s\n", D_ER);
			i--;
			continue;
		}
		if (!string_to_int(duration_str, &duration)
			|| duration < 10
			|| duration > 100)
		{
			printf("%s\n", DU_ER);
			i--;
			continue;
		}

		// Store the line info
		BusLine line = {0};
		strcpy(line.name, name);
		line.distance = distance;
		line.duration = duration;
		line_arr[i] = line;
	}

	// Perform the action, sort the lines or run the tests
	switch (action)
	{
		case BUBBLESORT:
		{
			bubble_sort(line_arr, line_arr + lines_num);
			break;
		}
		case QUICKSORT:
		{
			quick_sort(line_arr, line_arr + lines_num, sort_type);
			break;
		}
		case TEST:
		{
			run_tests(line_arr, line_arr + lines_num);
			free(line_arr);
			return EXIT_SUCCESS;
		}
		// Default case, free the allocated memory and return failure
		default:
		{
			free(line_arr);
			return EXIT_FAILURE;
		}
	}

	// Print the sorted lines
	print_array(line_arr, line_arr + lines_num);
	free(line_arr);

	return EXIT_SUCCESS;
}

/**
 * Convert a string to an integer, rounding the result
 *
 * @param str the string to convert
 * @param result the result of the conversion
 * @return 1 if the conversion was successful, 0 otherwise
 */
int string_to_int(const char *str, int *result)
{
	char *endptr;
	const long val = strtol(str, &endptr, 10);
	if (*endptr == '\0' || *endptr == '\n')
	{
		*result = (int) val;
		return 1; // Conversion Successful
	}
	return 0; // Conversion Failed
}
