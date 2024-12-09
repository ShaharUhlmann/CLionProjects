#include "memory_tests.h"
#include "markov_chain.h"
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

typedef void (*test_PrintFuncPtr)(void*);
typedef int (*test_CompFuncPtr)(void*, void*);
typedef void (*test_FreeFuncPtr)(void*);
typedef void* (*test_CopyFuncPtr)(void*);
typedef bool (*test_IsLastFuncPtr)(void*);

#define EMPTY -1
#define BOARD_SIZE 100
typedef struct Cell {
    int number; // Cell number 1-100
    int ladder_to;  // ladder_to represents the jump of the ladder in case there is one from this square
    int snake_to;  // snake_to represents the jump of the snake in case there is one from this square
    //both ladder_to and snake_to should be -1 if the Cell doesn't have them
} Cell;

bool my_is_last_cell(void* data)
{
    Cell* cell = (Cell*) data;
    return cell->number==BOARD_SIZE;
}

void my_print_cell_func(void* data)
{
    Cell* cell = (Cell*) data;
    if(my_is_last_cell(cell))
    {
        printf( "[%d]", cell->number);
        return;
    }
    if(cell->ladder_to != EMPTY)
    {
        printf( "[%d] -ladder to-> ", cell->number);
        return;
    }
    if(cell->snake_to != EMPTY)
    {
        printf( "[%d] -snake to-> ", cell->number);
        return;
    }
    printf("[%d] -> ", cell->number);
}

void my_free_cell_func(void* data)
{
    Cell * cell = (Cell*)data;
    if (cell == NULL)
    {
        return;
    }
    free(cell);
    cell=NULL;
}

Cell* my_copy_cell_func(void* data)
{
    Cell* original = (Cell*)data;
    if (original == NULL)
    {
        return NULL;
    }
    Cell * copy = malloc(sizeof(Cell));
    if(copy==NULL){
        return NULL;
    }
    copy->number=original->number;
    copy->ladder_to=original->ladder_to;
    copy->snake_to=original->snake_to;
    return copy;
}

int my_comp_cell_func(Cell* first_cell, Cell* sec_cell)
{
    return first_cell->number - sec_cell->number;
}

int main(){
    fail_realloc_after = 2;
    MarkovChain *my_chain = (MarkovChain *) malloc(sizeof(MarkovChain)); // 1 malloc
    if (my_chain==NULL){
        return EXIT_SUCCESS;
    }
    LinkedList *database = calloc(1, sizeof(LinkedList)); // 1 calloc
    if (database==NULL)
    {
        free(my_chain);
        return EXIT_SUCCESS;
    }

    *my_chain = (MarkovChain) {database, my_print_cell_func, (test_CompFuncPtr) my_comp_cell_func,
                               my_free_cell_func, (test_CopyFuncPtr)my_copy_cell_func, my_is_last_cell};
    Cell c1 = {1, EMPTY, EMPTY};
    Node* one = add_to_database(my_chain, &c1);
    if (one == NULL)
    {
        free_database(&my_chain);
        return EXIT_SUCCESS;
    }

    Cell c2 = {2, EMPTY, EMPTY};
    Node* two = add_to_database(my_chain, &c2);
    if (two == NULL)
    {
        free_database(&my_chain);
        return EXIT_SUCCESS;
    }

    Cell c3 = {3, EMPTY, EMPTY};
    Node* three = add_to_database(my_chain, &c3);
    if (three == NULL)
    {
        free_database(&my_chain);
        return EXIT_SUCCESS;
    }

    Cell c100 = {100, EMPTY, EMPTY};
    Node* hundred = add_to_database(my_chain, &c100);
    if (hundred == NULL)
    {
        free_database(&my_chain);
        return EXIT_SUCCESS;
    }

    int res = add_node_to_frequency_list(one->data, two->data); // SUCCESS
    if(res == EXIT_FAILURE)
    {
        free_database(&my_chain);
        return EXIT_SUCCESS;
    }

    res = add_node_to_frequency_list(one->data, hundred->data); // FAIL or SUCCESS (depend on implementation)
    if(res == EXIT_FAILURE)
    {
        if(one->data->frequency_list == NULL) // did not safe realloc
        {
            free_database(&my_chain);
            return EXIT_FAILURE;
        }
        free_database(&my_chain);
        return EXIT_SUCCESS;
    }

    res = add_node_to_frequency_list(two->data, three->data); // if prev succeeded then so will this
    if(res == EXIT_FAILURE)
    {
        free_database(&my_chain);
        return EXIT_SUCCESS;
    }

    res = add_node_to_frequency_list(two->data, hundred->data); // FAIL
    if(res == EXIT_FAILURE)
    {
        if(two->data->frequency_list == NULL) // did not safe realloc
        {
            free_database(&my_chain);
            return EXIT_FAILURE;
        }
        free_database(&my_chain);
        return EXIT_SUCCESS;
    }

    res = add_node_to_frequency_list(three->data, one->data);
    if(res == EXIT_FAILURE)
    {
        free_database(&my_chain);
        return EXIT_SUCCESS;
    }
}