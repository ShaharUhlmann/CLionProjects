#ifndef EX2_REPO_TESTBUSLINES_H
#define EX2_REPO_TESTBUSLINES_H
// write only between #define EX2_REPO_TESTBUSLINES_H and #endif
// EX2_REPO_TESTBUSLINES_H
#include "sort_bus_lines.h"

/**
 * function to check if an array of BusLine structs is sorted by distance
 *
 * @param start pointer to the first element of the array to be checked
 * @param end pointer to the element after the last element of the array
 * @return 1 if the array is sorted by distance, 0 otherwise
 */
int is_sorted_by_distance(const BusLine *start, const BusLine *end);

/**
 * function to check if an array of BusLine structs is sorted by duration
 *
 * @param start pointer to the first element of the array to be checked
 * @param end pointer to the element after the last element of the array
 * @return 1 if the array is sorted by duration, 0 otherwise
 */
int is_sorted_by_duration(const BusLine *start, const BusLine *end);

/**
 * function to check if an array of BusLine structs is sorted by name
 *
 * @param start pointer to the first element of the array to be checked
 * @param end pointer to the element after the last element of the array
 * @return 1 if the array is sorted by name, 0 otherwise
 */
int is_sorted_by_name(const BusLine *start, const BusLine *end);

/**
 * function to check if two arrays of BusLine structs are equal, i.e.,
 * have the same items (checks only the names)
 *
 * @param start_sorted pointer to the first element of the sorted array
 * @param end_sorted pointer to the element after the last of the sorted array
 * @param start_original pointer to the first element of the original array
 * @param end_original pointer to the element after the
 *                     last of the original array
 * @return 1 if the arrays are equal, 0 otherwise
 */
int is_equal(const BusLine *start_sorted,
             const BusLine *end_sorted,
             const BusLine *start_original,
             const BusLine *end_original);


/**
 * run tests of the sorting functions on an array of BusLine structs
 *
 * @param start pointer to the first element of the array to be tested
 * @param end pointer to the element after the last of the array to be tested
 */
void run_tests(const BusLine *start, const BusLine *end);

// write only between #define EX2_REPO_TESTBUSLINES_H and #endif
// EX2_REPO_TESTBUSLINES_H
#endif //EX2_REPO_TESTBUSLINES_H
