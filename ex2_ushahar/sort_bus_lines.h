#ifndef EX2_REPO_SORTBUSLINES_H
#define EX2_REPO_SORTBUSLINES_H
// write only between #define EX2_REPO_SORTBUSLINES_H and #endif
// EX2_REPO_SORTBUSLINES_H

#include <string.h>

#define NAME_LEN 21

/**
 * function to sort an array of BusLine structs by name using bubble sort
 *
 * @param start pointer to the first element of the array to be sorted
 * @param end pointer to the element after the last element of the array
 */
typedef struct BusLine
{
 char name[NAME_LEN];
 int distance, duration;
} BusLine;

typedef enum SortType
{
 DISTANCE,
 DURATION
} SortType;


/**
 * function to sort an array of BusLine structs by name using bubble sort
 *
 * @param start pointer to the first element of the array to be sorted
 * @param end pointer to the element after the last element of the array
 */
void bubble_sort(BusLine *start, BusLine *end);

/**
 * function to partition an array of BusLine structs
 *
 * @param start pointer to the first element of the array to be sorted
 * @param end pointer to the element after the last element of the array
 * @param sort_type enum value to determine the sorting type
 * @return
 */
BusLine *partition(BusLine *start, BusLine *end, SortType sort_type);

/**
 * function to sort an array of BusLine structs using quick sort
 *
 * @param start pointer to the first element of the array to be sorted
 * @param end pointer to the element after the last element of the array
 * @param sort_type enum value to determine the sorting type
 */
void quick_sort(BusLine *start, BusLine *end, SortType sort_type);


/**
 * function to print an array of BusLine structs
 *
 * @param bus_line pointer to the first element of the array to be printed
 * @param end pointer to the element after the last element of the array
 */
void print_array(BusLine *bus_line, const BusLine *end);

// write only between #define EX2_REPO_SORTBUSLINES_H and #endif
//EX2_REPO_SORTBUSLINES_H
#endif //EX2_REPO_SORTBUSLINES_H
