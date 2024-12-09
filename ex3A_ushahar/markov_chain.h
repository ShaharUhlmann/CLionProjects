#ifndef _MARKOV_CHAIN_H_
#define _MARKOV_CHAIN_H_

#include "linked_list.h"
#include <stdio.h>  // For printf(), sscanf()
#include <stdlib.h> // For malloc()
#include <stdbool.h> // for bool

//Don't change the macros!
#define ALLOCATION_ERROR_MESSAGE "Allocation failure: Failed to allocate"\
 " new memory\n"

typedef struct MarkovChain
{
	LinkedList* database;
} MarkovChain;

typedef struct MarkovNode
{
	char* data;
	struct MarkovNodeFrequency* frequency_list;
	int frequency_list_size;
	int probability_sum;
	// added for easier access to the sum of all frequencies
	// any other field you need
} MarkovNode;

typedef struct MarkovNodeFrequency
{
	struct MarkovNode* markov_node;
	int frequency;
	// any other fields you need
} MarkovNodeFrequency;

/**
 * Check if data_ptr is in database. If so, return the Node wrapping it in
 * the markov_chain, otherwise return NULL.
 * @param markov_chain the chain to look in its database
 * @param data_ptr the data to look for
 * @return Pointer to the Node wrapping given data, NULL if state not in
 * database.
 */
Node* get_node_from_database(MarkovChain* markov_chain, char* data_ptr);

/**
 * If data_ptr in markov_chain, return it's node. Otherwise, create new
 * node, add to end of markov_chain's database and return it.
 * @param markov_chain the chain to look in its database
 * @param data_ptr the data to look for
 * @return Node wrapping given data_ptr in given chain's database,
 * returns NULL in case of memory allocation failure.
 */
Node* add_to_database(MarkovChain* markov_chain, char* data_ptr);

/**
 * Add the second markov_node to the frequency list of the first markov_node.
 * If already in list, update it's occurrence frequency value.
 * @param first_node
 * @param second_node
 * @return success/failure: 0 if the process was successful, 1 if in
 * case of allocation error.
 */
int add_node_to_frequency_list(MarkovNode* first_node,
                               MarkovNode* second_node);

/**
 * Free markov_chain and all of it's content from memory
 * @param markov_chain markov_chain to free
 */
void free_database(MarkovChain** markov_chain);

/**
 * Get one random MarkovNode from the given markov_chain's database.
 * @param markov_chain
 * @return the random MarkovNode
 */
MarkovNode* get_first_random_node(MarkovChain* markov_chain);

/**
 * Choose randomly the next MarkovNode, depend on it's occurrence frequency.
 * @param cur_markov_node current MarkovNode
 * @return the next random MarkovNode
 */
MarkovNode* get_next_random_node(MarkovNode* cur_markov_node);

/**
 * Receive markov_chain, generate and print random sentence out of it. The
 * sentence must have at least 2 words in it.
 * @param first_node markov_node to start with
 * @param max_length maximum length of chain to generate
 */
void generate_tweet(MarkovNode* first_node, int max_length);

/**
 * Check if the given markov_node is valid.
 * @param markov_node the node to check
 * @return 0 if the node is valid, 1 otherwise
 */
int check_markov_node(MarkovNode* markov_node);

/**
 * Check if the given node is valid.
 * @param node the node to check
 * @return 0 if the node is valid, 1 otherwise
 */
int check_node(Node* node);


#endif /* _MARKOV_CHAIN_H_ */
