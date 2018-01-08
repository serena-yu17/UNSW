/*
define operator^ as power

Task 1 complexity: O(m^2) * O(n^2)
 The levenstein distance algorithm is O(m*m), and it was executed for worst n(n-1)/2 times for comparison between each pairs of words.

 Task 2 complexity O(n^2)
 DFS search complexity O(V+E), and here V = n, E can be worst at n^2, so we search for O(n^2) times.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

 //max word length
#define BUFFER_SIZE 19


int** buildChains(char**, int, int*);
int levensDist(char*, char*);
int* buildCandidates(int, char**, int, int*);
int*** searchChain(int**, char**, int, int*, int*, size_t*);

int imin(int a, int b, int c)
{
	if (a <= b && a <= c)
		return a;
	if (b <= a && b <= c)
		return b;
	return c;
}


int main()
{
	//input
	printf("Enter a number: ");
	int wordCount;
	char numBuffer[6];			//<= 1000 
	fgets(numBuffer, 6, stdin);
	wordCount = atoi(numBuffer);
	if (wordCount <= 0 || wordCount > 1000)
	{
		puts("Invalid input, giving up...");
		return 1;
	}
	char** words = (char**)malloc(wordCount * sizeof(char*));
	for (int i = 0; i < wordCount; i++)
	{
		words[i] = (char*)malloc(BUFFER_SIZE + 1);
		printf("Enter word: ");
		fgets(words[i], BUFFER_SIZE, stdin);
		//Remove the \n
		if (words[i][strlen(words[i]) - 1] == '\n')
			words[i][strlen(words[i]) - 1] = '\0';
	}
	//end input

	//calculate individual chains for each word
	//lengthOfChain: records how many words can be chained on the specific word at position i. 
	//That is, size of each int array in chains. 
	int* lengthOfChain = (int*)malloc(wordCount * sizeof(int));
	memset(lengthOfChain, 0, wordCount * sizeof(int));
	int** chains = buildChains(words, wordCount, lengthOfChain);

	//Print individual chains
	for (int i = 0; i < wordCount; i++)
	{
		printf("\n%s:", words[i]);
		for (int j = 0; j < lengthOfChain[i]; j++)
			if (chains[i][j])
				printf(" %s", words[chains[i][j]]);
	}

	//Search for the longest chain
	int maxLength = 0;
	size_t countChains = 0;
	int*** longestChains = searchChain(chains, words, wordCount, lengthOfChain, &maxLength, &countChains);

	//Print longest chains
	printf("\n\nMaximum chain length: %d\n", maxLength);
	printf("Maximal chains:\n");
	for (size_t i = 0; i < countChains; i++)
	{
		int* chainWords = (*longestChains)[i];
		if (chainWords)
		{
			for (int j = 0; j < maxLength; j++)
			{
				if (j)
					printf(" -> ");
				printf("%s", words[chainWords[j]]);
			}
			printf("\n");
			free(chainWords);
		}
	}

	//clean up
	for (int i = 0; i < wordCount; i++)
	{
		free(words[i]);
		free(chains[i]);
	}
	free(*longestChains);
	free(longestChains);
	free(chains);
	free(lengthOfChain);
	free(words);
	//

	getchar();
	return 0;
}

int levensDist(char* first, char* second)
{
	//Iterative Levenstein distain algorith, used to calculate distance between words.	
	int len1 = strlen(first);
	int len2 = strlen(second);
	int* markRow1 = (int*)malloc((len2 + 1) * sizeof(int));
	int* markRow2 = (int*)malloc((len2 + 1) * sizeof(int));
	for (int i = 0; i <= len2; i++)
		markRow1[i] = i;
	for (int i = 0; i < len1; i++)
	{
		markRow2[0] = i + 1;
		for (int j = 0; j < len2; j++)
		{
			int cost = 0;
			if (first[i] != second[j])
				cost = 1;				  //replacement cost was set to 1
			markRow2[j + 1] = imin(markRow2[j] + 1, markRow1[j + 1] + 1, markRow1[j] + cost);
		}
		int* tmp = markRow2;
		markRow2 = markRow1;
		markRow1 = tmp;
	}
	int distance = markRow1[len2];

	//clean up
	free(markRow1);
	free(markRow2);
	//

	return distance;
}

int* buildCandidates(int start, char** words, int wordCount, int* lengthOfChain)
{
	int* candidatesOfWord = NULL;
	int pos = 0;
	if (start < wordCount - 1)
	{
		candidatesOfWord = (int*)malloc((wordCount - start - 1) * sizeof(int));
		char* target = words[start];
		int len = strlen(target);
		for (int i = start + 1; i < wordCount; i++)
		{
			if (abs(strlen(words[i]) - len) < 2 && levensDist(target, words[i]) == 1)
				candidatesOfWord[pos++] = i;
		}
	}
	*lengthOfChain = pos;
	return candidatesOfWord;
}

int** buildChains(char** words, int wordCount, int* lengthOfChain)
{
	int** chains = (int**)malloc(wordCount * sizeof(int*));
	for (int i = 0; i < wordCount; i++)
		chains[i] = buildCandidates(i, words, wordCount, &lengthOfChain[i]);
	return chains;
}


int*** searchChain(int** chains, char** words, int wordCount, int* lengthOfChain, int* maxLength, size_t* size)
{
	//iterative DFS to looking for the longest combination of chains
	int* stack = (int*)malloc(sizeof(int) * (wordCount + 1));
	int* used = (int*)malloc(sizeof(int)*(wordCount + 1));
	memset(used, 0, sizeof(int) * (wordCount + 1));
	int stackSize = 0;
	stack[stackSize++] = wordCount;		//Dummy head of stack
	size_t countChains = 0;
	size_t capacity = 0;
	int*** longestChains = (int***)malloc(sizeof(*longestChains));
	*longestChains = NULL;
	while (stackSize)
	{
		int top = stack[stackSize - 1];		//top of stack
		if (top == wordCount && used[top] < wordCount)		  // used[wordCount] records the first words used
		{
			stack[stackSize++] = used[top];
			used[top]++;
		}
		else if (top < wordCount && used[top] < lengthOfChain[top])
		{
			stack[stackSize++] = chains[top][used[top]];
			used[top]++;
		}
		else
		{
			if (stackSize - 1 > *maxLength)
			{
				*maxLength = stackSize - 1;
				//remove all existing chains
				if (*longestChains && countChains) {
					for (int i = 0; i < countChains; i++)
					{
						free((*longestChains)[i]);
						(*longestChains)[i] = NULL;
					}
					if (capacity > 512)
					{
						free((*longestChains));
						(*longestChains) = NULL;
						capacity = 0;
					}
				}
				if (!(*longestChains))
				{
					capacity = 256;
					*longestChains = (int**)malloc(sizeof(int*) * capacity);
				}
				//The stack makes the first new chain
				(*longestChains)[0] = (int*)malloc(sizeof(int) * (stackSize - 1));
				memcpy((*longestChains)[0], stack + 1, sizeof(int) * (stackSize - 1));
				countChains = 1;
			}
			else if (stackSize - 1 == *maxLength)
			{
				// If chains not allocated, allocate memory
				if (!(*longestChains))
				{
					capacity = 256;
					*longestChains = (int**)malloc(sizeof(int*) * capacity);
				}
				//If the array is full, expand
				if (countChains == capacity)
				{
					capacity *= 2;
					int** temp = (int**)realloc((void*)(*longestChains), sizeof(int*) * capacity);
					if (!temp)
					{
						printf("Error: realloc failed at word[%d]: %s.", stack[1], words[stack[1]]);
						return NULL;
					}
					*longestChains = temp;
				}
				(*longestChains)[countChains] = (int*)malloc(sizeof(int) * (stackSize - 1));
				memcpy((*longestChains)[countChains], stack + 1, sizeof(int) * (stackSize - 1));
				countChains++;
			}
			used[top] = 0;
			stackSize--;
		}
	}

	//clean up
	free(stack);
	free(used);
	//
	*size = countChains;
	return longestChains;
}

