#include <string.h>

int snakes_main(int argc, char * argv[]);
int tweets_main(int argc, char * argv[]);

int main (int argc, char * argv[])
{
  // argv[1]  decides which main to run
  if (!strcmp(argv[1], "snakes"))
	{
	  snakes_main (argc - 1, argv + 1);
	}
  else
	{
	  /*run tweets test */
	  tweets_main (argc - 1, argv + 1);
	}
}