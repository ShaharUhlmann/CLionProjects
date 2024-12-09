//Don't change the macros!
#define FILE_PATH_ERROR "Error: incorrect file path"
#define NUM_ARGS_ERROR "Usage: invalid number of arguments"

#define DELIMITERS " \n\t\r"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "markov_chain.h"

int fill_database(FILE* fp, int words_to_read, MarkovChain* markov_chain);

/**
 * accepts 3 or 4 arguments from the user
 * argv[1] - seed value for random number generator
 * argv[2] - amount of "tweets" (generated sentences) to generate
 * argv[3] - path to the file containing Text Corpus
 * optional argv[4] - amount of words to read from the file
 * prints the generated tweets to stdout
 *
 * @param argc
 * @param argv
 * @return EXIT_SUCCESS if the program ran successfully,
 * EXIT_FAILURE otherwise
 */
int main(const int argc, char* argv[])
{
	char* seed_ptr = NULL;
	int seed_value = strtol(argv[1], &seed_ptr, 10);
	srand(seed_value);
	if (argc != 4 && argc != 5)
	{
		printf("%s\n", NUM_ARGS_ERROR);
		return EXIT_FAILURE;
	}
	//check if the file path is correct:
	//if the file path is incorrect,
	//print FILE_PATH_ERROR to stdout and return EXIT_FAILURE
	FILE* file = fopen(argv[3], "r");
	if (file == NULL)
	{
		printf("%s\n", FILE_PATH_ERROR);
		return EXIT_FAILURE;
	}
	int words_to_read = 0;
	if (argc == 5)
	{
		char* endptr;
		words_to_read = strtol(argv[4], &endptr, 10);
	}
	MarkovChain* markov_chain = calloc(1, sizeof(MarkovChain));
	if (markov_chain == NULL)
	{
		fclose(file);
		return EXIT_FAILURE;
	}
	markov_chain->database = calloc(1, sizeof(LinkedList));
	if (fill_database(file, words_to_read, markov_chain) == EXIT_FAILURE)
	{
		fclose(file);
		free_database(&markov_chain);
		return EXIT_FAILURE;
	}
	char* endptr;
	long num_tweets = strtol(argv[2], &endptr, 10);
	if (*endptr != '\0' || num_tweets <= 0)
	{
		printf("%s\n", NUM_ARGS_ERROR);
		return EXIT_FAILURE;
	}

	for (int i = 0; i < num_tweets; i++)
	{
		printf("Tweet %d: ", i + 1);
		MarkovNode* node = get_first_random_node(markov_chain);
		generate_tweet(node, 20);
		putchar('\n');
	}
	free_database(&markov_chain);
	fclose(file);
	return EXIT_SUCCESS;
}


int fill_database(FILE* fp, int words_to_read, MarkovChain* markov_chain)
{
	if (fp == NULL)
	{
		return EXIT_FAILURE;
	}
	assert(fp != NULL);
	assert(markov_chain != NULL);
	assert(words_to_read >= 0);

	size_t buffer_size = 1000;
	char* line = (char*)calloc(buffer_size, sizeof(char));
	if (line == NULL)
	{
		return EXIT_FAILURE;
	}

	int words_read = 0;
	Node* current_node = NULL;
	Node* next_node = NULL;

	while (fgets(line, buffer_size, fp) != NULL)
	{
		char* word = strtok(line, DELIMITERS);
		while (word != NULL)
		{
			if (strlen(word) > 0) // Ensure the word is not empty
			{
				next_node = add_to_database(markov_chain, word);
				if (next_node == NULL)
				{
					free(line);
					return EXIT_FAILURE;
				}
				if (current_node != NULL)
				{
					if (add_node_to_frequency_list(
							current_node->data,
							next_node->data) == EXIT_FAILURE)
					{
						free(line);
						return EXIT_FAILURE;
					}
				}
				current_node = next_node;
				words_read++;
				if (words_to_read != 0 && words_read >= words_to_read)
				{
					free(line);
					return EXIT_SUCCESS;
				}
			}
			word = strtok(NULL, DELIMITERS);
		}
	}
	free(line);
	return EXIT_SUCCESS;
}
