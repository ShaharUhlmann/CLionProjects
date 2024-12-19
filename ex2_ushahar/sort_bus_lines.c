#include "sort_bus_lines.h"

#include <stdbool.h>
#include <stdio.h>


void bubble_sort(BusLine *start, BusLine *end)
{
	for (BusLine *i = start; i < end; i++)
	{
		for (BusLine *j = start; j < end - 1; j++)
		{
			if (strcmp(j->name, (j + 1)->name) > 0)
			{
				const BusLine temp = *j;
				*j = *(j + 1);
				*(j + 1) = temp;
			}
		}
	}
}


BusLine *partition(BusLine *start, BusLine *end, SortType sort_type)
{
	BusLine *i = start - 1;
	BusLine *j = end;
	const BusLine pivot = *start;

	while (true)
	{
		do
		{
			i++;
		} while (sort_type == DISTANCE
					 ? i->distance < pivot.distance
					 : i->duration < pivot.duration);

		do
		{
			j--;
		} while (sort_type == DISTANCE
					 ? j->distance > pivot.distance
					 : j->duration > pivot.duration);

		if (i >= j)
		{
			return j;
		}

		const BusLine temp = *i;
		*i = *j;
		*j = temp;
	}
}


void quick_sort(BusLine *start, BusLine *end, SortType sort_type)
{
	if (start < end - 1)
	{
		BusLine *p = partition(start, end, sort_type);
		quick_sort(start, p + 1, sort_type);
		quick_sort(p + 1, end, sort_type);
	}
}


void print_array(BusLine *bus_line, const BusLine *end)
{
	for (BusLine *i = bus_line; i < end; i++)
	{
		printf("%s,%d,%d\n", i->name, i->distance, i->duration);
	}
}
