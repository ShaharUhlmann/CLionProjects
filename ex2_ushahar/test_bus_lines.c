#include "test_bus_lines.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TST_ERR " FAILED: The array is not sorted by "
#define CMP_PS " PASSED: The array has the same items after sorting"
#define TST_PS " PASSED: The array is sorted by "
#define CMP_ERR " FAILED: The array doesnt have the same items after sorting"

int is_sorted_by_distance(const BusLine *start, const BusLine *end)
{
	for (const BusLine *current = start; current < end - 1; current++)
	{
		if (current->distance > (current + 1)->distance)
		{
			return 0; // Not sorted
		}
	}
	return 1; // Sorted
}

int is_sorted_by_duration(const BusLine *start, const BusLine *end)
{
	for (const BusLine *current = start; current < end - 1; current++)
	{
		if (current->duration > (current + 1)->duration)
		{
			return 0; // Not sorted
		}
	}
	return 1; // Sorted
}

int is_sorted_by_name(const BusLine *start, const BusLine *end)
{
	for (const BusLine *current = start; current < end - 1; current++)
	{
		if (strcmp(current->name, (current + 1)->name) > 0)
		{
			return 0; // Not sorted
		}
	}
	return 1; // Sorted
}

int is_equal(const BusLine *start_sorted,
			 const BusLine *end_sorted,
			 const BusLine *start_original,
			 const BusLine *end_original)
{
	if (end_sorted - start_sorted != end_original - start_original)
	{
		// The arrays have different sizes
		printf("%ld %ld",
			   end_sorted - start_sorted,
			   end_original - start_original);
		return 0; // Not equal
	}
	for (const BusLine *original = start_original; original < end_original;
		 original++)
	{
		// Check if the current element is in the sorted array
		int found = 0;
		for (const BusLine *sorted = start_sorted;
			 sorted < end_sorted;
			 sorted++)
		{
			if (strcmp(original->name, sorted->name) == 0)
			{
				found = 1;
				break;
			}
		}
		if (!found)
		{
			// The current element is not in the sorted array
			printf("%s", original->name);
			return 0; // Not equal
		}
	}
	return 1; // Equal
}

void run_tests(const BusLine *start, const BusLine *end)
{
	BusLine *sorted = malloc((end - start) * sizeof(BusLine));
	if (sorted == NULL)
	{
		return;
	}
	memcpy(sorted, start, (end - start) * sizeof(BusLine));

	quick_sort(sorted, sorted + (end - start), DISTANCE);
	printf("TEST 1%s%s\n",
		   is_sorted_by_distance(sorted, sorted + (end - start))
			   ? TST_PS
			   : TST_ERR,
		   "distance");
	printf("TEST 2%s\n",
		   is_equal(sorted,
					sorted + (end - start),
					start,
					end)
			   ? CMP_PS
			   : CMP_ERR);

	memcpy(sorted, start, (end - start) * sizeof(BusLine));
	quick_sort(sorted, sorted + (end - start), DURATION);
	printf("TEST 3%s%s\n",
		   is_sorted_by_duration(sorted, sorted + (end - start))
			   ? TST_PS
			   : TST_ERR,
		   "duration");
	printf("TEST 4%s\n",
		   is_equal(sorted,
					sorted + (end - start),
					start,
					end)
			   ? CMP_PS
			   : CMP_ERR);

	memcpy(sorted, start, (end - start) * sizeof(BusLine));
	bubble_sort(sorted, sorted + (end - start));
	printf("TEST 5%s%s\n",
		   is_sorted_by_name(sorted, sorted + (end - start))
			   ? TST_PS
			   : TST_ERR,
		   "name");
	printf("TEST 6%s\n",
		   is_equal(sorted,
					sorted + (end - start),
					start,
					end)
			   ? CMP_PS
			   : CMP_ERR);

	free(sorted);
}
