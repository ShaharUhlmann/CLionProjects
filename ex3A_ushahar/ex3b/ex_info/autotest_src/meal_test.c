#include <string.h> // For strlen(), strcmp(), strcpy()
#include "markov_chain.h"
#include <stdbool.h>

typedef void (*meal_PrintFuncPtr)(void*);
typedef int (*meal_CompFuncPtr)(void*, void*);
typedef void (*meal_FreeFuncPtr)(void*);
typedef void* (*meal_CopyFuncPtr)(void*);
typedef bool (*meal_IsLastFuncPtr)(void*);

#define MAX(X, Y) (((X) < (Y)) ? (Y) : (X))

#define EMPTY -1
#define MAX_GENERATION_LENGTH 3

#define DECIMAL 10

#define NUM_ARGS 3

/* argv indexes */
#define SEED_ARG_INDEX 1
#define NUM_MEALS_INDEX 2

#define FILL_DATABASE_ERROR_MESSAGE "Error: Failed to create the database.\n"

#define NUM_ARGS_ERROR "Usage: invalid number of arguments."

/**
 * represents the transitions by ladders and snakes in the game
 * each tuple (x,y) represents a ladder from x to if x<y or a snake otherwise
 */

typedef enum CourseType {Appetizer, First, Second, Main, Dessert} CourseType;

/**
 * struct represents a Cell in the game board
 */
typedef struct Course {
    CourseType type;
    char* description;
    int calories;
} Course;

/** Error handler **/
int handle_error_meal(char *error_msg, MarkovChain **database)
{
    printf("%s", error_msg);
    if (database != NULL)
    {
        free_database(database);
    }
    return EXIT_FAILURE;
}

bool is_last_course(void* data)
{
    Course * course = (Course *) data;
    return course->type==Dessert;
}

void print_course_func(void* data)
{
    Course * course = (Course *) data;
    printf( "description: %s, ", course->description);
    printf( "calories: %d, ", course->calories);
    switch (course->type)
    {
        case Appetizer:
            printf( "type: Appetizer\n");
            break;
        case First:
            printf( "type: First\n");
            break;
        case Second:
            printf( "type: Second\n");
            break;
        case Main:
            printf( "type: Main\n");
            break;
        case Dessert:
            printf( "type: Dessert\n");
            printf( "We hope you had a nice meal!\n");
            break;
    }
}

void free_course_func(void* data)
{
    Course * course = (Course *) data;
    if (course == NULL)
    {
        return;
    }
    if(course->description!=NULL)
    {
        free(course->description);
    }
    free(course);
    course=NULL;
}

Course * copy_course_func(void* data)
{
    Course * original = (Course *) data;
    if (original == NULL)
    {
        return NULL;
    }
    Course * copy = malloc(sizeof(Course));
    if(copy==NULL)
    {
        return NULL;
    }
    copy->type=original->type;
    copy->calories=original->calories;
    copy->description= malloc(strlen(original->description)+1);
    strcpy(copy->description, original->description);
    return copy;
}

int comp_course_func(Course * first_cell, Course * sec_cell)
{
    if((first_cell->type-sec_cell->type)==0){
        return strcmp(first_cell->description, sec_cell->description);
    }
    return first_cell->type - sec_cell->type;
}

int create_courses(Course* courses[10])
{
    for(int i=0; i<10; i++){
        courses[i] = (Course *) malloc(sizeof(Course));
        if (courses[i] == NULL)
        {
            printf(ALLOCATION_ERROR_MESSAGE);
            for(int j=0; j<i; j++)
            {
                free(courses[j]);
            }
            return EXIT_FAILURE;
        }
    }
    *(courses[0])=(Course){Appetizer, "appetizer_a", 100};
    *(courses[1])=(Course){Appetizer, "appetizer_b", 200};
    *(courses[2])=(Course){First, "first_a", 50};
    *(courses[3])=(Course){First, "first_b", 60};
    *(courses[4])=(Course){Second, "second_a", 90};
    *(courses[5])=(Course){Second, "second_b", 20};
    *(courses[6])=(Course){Main, "main_a", 500};
    *(courses[7])=(Course){Main, "main_b", 600};
    *(courses[8])=(Course){Dessert, "dessert_a", 110};
    *(courses[9])=(Course){Dessert, "dessert_b", 220};
    return EXIT_SUCCESS;
}


/**
 * fills database
 * @param markov_chain
 * @return EXIT_SUCCESS or EXIT_FAILURE
 */
int fill_database_meal(MarkovChain *markov_chain)
{
    Course* courses[10];
    if(create_courses(courses)==EXIT_FAILURE)
    {
        return EXIT_FAILURE;
    }
    MarkovNode* prev_ptr=NULL;
    for(int i=0; i<10; i++)
    {
        add_to_database(markov_chain,courses[i]);
    }
    for(int i=0; i<8; i++)
    {
        prev_ptr=(MarkovNode*) get_node_from_database(markov_chain,courses[i])->data;
        for(int j=i+1; j<10; j++)
        {
            if(courses[i]->type != courses[j]->type)
            {
                MarkovNode * to_add = get_node_from_database(markov_chain, courses[j])->data;
                add_node_to_frequency_list(prev_ptr, to_add);
            }
        }
    }
    for(int i=0; i<10; i++){
        free(courses[i]);
    }
    return EXIT_SUCCESS;
}



/**
 * @param argc num of arguments
 * @param argv 1) Seed
 *             2) Number of sentences to generate
 * @return EXIT_SUCCESS or EXIT_FAILURE
 */
int meal_main(int argc, char *argv[])
{
// Check arguments
    if (argc != NUM_ARGS)
    {
        return handle_error_meal(NUM_ARGS_ERROR, NULL);
    }
    // Create markov_chain struct:
    MarkovChain *my_chain = (MarkovChain *) malloc(sizeof(MarkovChain));
    if (my_chain == NULL)
    {
        return handle_error_meal(ALLOCATION_ERROR_MESSAGE, NULL);
    }
    // Create database
    LinkedList *database = calloc(1, sizeof(LinkedList));
    if (database == NULL)
    {
        return handle_error_meal(ALLOCATION_ERROR_MESSAGE, &my_chain);
    }
    *my_chain = (MarkovChain) {database, print_course_func, (meal_CompFuncPtr) comp_course_func,
                               free_course_func, (meal_CopyFuncPtr)copy_course_func, is_last_course};
    // fill database
    if (fill_database_meal(my_chain) == EXIT_FAILURE)
    {
        return handle_error_meal(FILL_DATABASE_ERROR_MESSAGE, &my_chain);
    }

    // Set seed
    srand(strtol(argv[SEED_ARG_INDEX], NULL, DECIMAL));

    // Generate sentences
    int amount_of_meals_to_generate = strtol(argv[NUM_MEALS_INDEX], NULL, DECIMAL);
    for (int i = 1; i <= amount_of_meals_to_generate; i++)
    {

        printf("Meal %d:\n", i);
        MarkovNode *firstNode = get_first_random_node(my_chain);
        generate_random_sequence(my_chain, firstNode, MAX_GENERATION_LENGTH);
        printf("\n");
    }

    // Free memory
    free_database(&my_chain);
    return EXIT_SUCCESS;
}
