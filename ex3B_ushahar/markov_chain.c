#include "markov_chain.h"

#include <assert.h>
#include <string.h>
#include <stdlib.h>
//check for git

int get_random_number(int max_number)
{
    return rand() % max_number;
}


Node* get_node_from_database(MarkovChain *markov_chain, void *data_ptr)
{
    assert(data_ptr != NULL);
    assert(markov_chain != NULL);
    assert(markov_chain->database != NULL);
    Node *current_node = markov_chain->database->first;
    while(current_node)
    {
        if(current_node->data == NULL)
        {
            return current_node;
        }
        if(current_node->data->data == NULL)
        {
            return NULL;
        }
        if(markov_chain->comp_func(current_node->data->data, data_ptr) == 0)
        {
            return current_node;
        }
        current_node = current_node->next;
    }
    return NULL;
}


Node* add_to_database(MarkovChain *markov_chain, void *data_ptr)
{
    // add to database using add function
    if(markov_chain == NULL)
    {
        return NULL;
    }
    if(markov_chain->database == NULL)
    {
        return NULL;
    }
    Node *node = get_node_from_database(markov_chain, data_ptr);
    if(node != NULL)
    {
        return node;
    }
    MarkovNode *markov_node = (MarkovNode *) calloc(1, sizeof(MarkovNode));
    if(markov_node == NULL)
    {
        return NULL;
    }
    markov_node->data = markov_chain->copy_func(data_ptr);
    if(add(markov_chain->database, markov_node) == EXIT_FAILURE)
    {
        free(markov_node->frequency_list);
        free(markov_node);
        return NULL;
    }
    assert(markov_chain->comp_func(markov_node->data,
                markov_chain->database->last->data->data) !=
            0);
    return markov_chain->database->last;
}


int add_node_to_frequency_list(MarkovNode *first_node,
                               MarkovNode *second_node)
{
    if(first_node->frequency_list == NULL)
    {
        first_node->frequency_list = calloc(1, sizeof(MarkovNodeFrequency));
        if(first_node->frequency_list == NULL)
        {
            return EXIT_FAILURE;
        }

        first_node->frequency_list->markov_node = second_node;
        first_node->frequency_list->frequency = 1;
        first_node->frequency_list_size = 1;
        first_node->probability_sum = 1;
        return EXIT_SUCCESS;
    }

    for(int i = 0; i < first_node->frequency_list_size; i++)
    {
        if(first_node->frequency_list[i].markov_node == second_node)
        {
            first_node->frequency_list[i].frequency++;
            first_node->probability_sum++;
            return EXIT_SUCCESS;
        }
    }

    MarkovNodeFrequency *new_frequency_list = realloc(
            first_node->frequency_list,
            sizeof(MarkovNodeFrequency) *
            (first_node->frequency_list_size + 1));
    if(new_frequency_list == NULL)
    {
        return EXIT_FAILURE;
    }

    first_node->frequency_list = new_frequency_list;
    first_node->frequency_list[first_node->frequency_list_size].markov_node =
            second_node;
    first_node->frequency_list[first_node->frequency_list_size].frequency = 1;
    first_node->frequency_list_size++;
    first_node->probability_sum++;
    return EXIT_SUCCESS;
}


void free_database(MarkovChain **chain_ptr)
{
    if(chain_ptr == NULL)
    {
        return;
    }
    if(*chain_ptr == NULL)
    {
        chain_ptr = NULL;
        return;
    }
    if((*chain_ptr)->database == NULL)
    {
        free(*chain_ptr);
        *chain_ptr = NULL;
        return;
    }
    LinkedList database = *(*chain_ptr)->database;
    if(database.first == NULL)
    {
        free(*chain_ptr);
        *chain_ptr = NULL;
        return;
    }
    Node *current_node = database.first;
    while(current_node != NULL)
    {
        Node *next_node = current_node->next;
        free(current_node->data->frequency_list);
        (*chain_ptr)->free_data(current_node->data->data);
        free(current_node->data);
        free(current_node);
        current_node = next_node;
    }
    database.first = NULL;
    if(database.last != NULL)
    {
        database.last = NULL;
    }
    free((*chain_ptr)->database);
    free(*chain_ptr);
    *chain_ptr = NULL;
}


MarkovNode* get_first_random_node(MarkovChain *markov_chain)
{
    if(markov_chain == NULL)
    {
        return NULL;
    }
    if(markov_chain->database == NULL)
    {
        return NULL;
    }
    if(markov_chain->database->size == 0)
    {
        return NULL;
    }
    while(true)
    {
        // Get random node from database
        int random_number = get_random_number(markov_chain->database->size);
        Node *random_node = markov_chain->database->first;
        while(random_number-- > 0)
        {
            random_node = random_node->next;
            if(random_node->next == NULL)
            {
                return NULL;
            }
        }
        if(check_node(random_node) == EXIT_SUCCESS)
        {
            // check if the node is not a sentence ending node
            if(markov_chain->is_last(random_node->data))
            {
                return random_node->data;
            }
        }
    }
}


MarkovNode* get_next_random_node(MarkovNode *cur_markov_node)
{
    if(cur_markov_node == NULL)
    {
        return NULL;
    }
    // Get random number between 0 and cur_markov_node->probability_sum
    if(cur_markov_node->probability_sum == 0)
    {
        return NULL;
    }
    int random_number = get_random_number(cur_markov_node->probability_sum);
    for(int i = 0; i < cur_markov_node->frequency_list_size; i++)
    {
        random_number -= cur_markov_node->frequency_list[i].frequency;
        if(random_number < 0)
        {
            return cur_markov_node->frequency_list[i].markov_node;
        }
    }
    return NULL;
}


void generate_random_sequence(MarkovChain *markov_chain,
                              MarkovNode *first_node, int max_length)
{
    if(check_markov_node(first_node) == EXIT_FAILURE)
    {
        return;
    }
    // Print the first word
    markov_chain->print_func(first_node);
    // Print the rest of the words
    MarkovNode *current_node = first_node;
    while(max_length-- > 0)
    {
        current_node = get_next_random_node(current_node);
        if(current_node == NULL)
        {
            break;
        }
        markov_chain->print_func(current_node->data);
        if(current_node->data != NULL)
        {
            if(markov_chain->is_last(current_node->data))
            {
                break;
            }
        }
    }
}


int check_markov_node(MarkovNode *markov_node)
{
    if(markov_node == NULL)
    {
        return EXIT_FAILURE;
    }
    if(markov_node->data == NULL)
    {
        return EXIT_FAILURE;
    }
    if(markov_node->frequency_list == NULL)
    {
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}

//
//int check_node(Node *node)
//{
//    if(node == NULL)
//    {
//        return EXIT_FAILURE;
//    }
//    return check_markov_node(node->data);
//}