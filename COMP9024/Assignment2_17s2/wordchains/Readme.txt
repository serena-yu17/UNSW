
A word chain is a sequence of k ≥ 1 words:

ω1 → ω2 → ω3 → … → ωk-1 → ωk
in which
words appear in alphabetical order, and
each word ωi+1 is related to its predecessor ωi by
changing one letter, e.g.  bear → beer
or adding or removing one letter, e.g.  compete → complete  or  bear → ear.
An example is the following word chain of length k = 6:

bear → dear → ear → ears → hears → hearts
Your task is to write a program for computing the longest word chains that can be built from a given collection of words.

Your program should:

prompt the user to input
a positive number n
n words
Task 1: compute and output, for each word ω, all words that could immediately follow ω in a word chain,
Task 2: compute and output
the maximum length of a word chain that can be built from the given words,
all word chains of maximum length that can be built from the given words.
Your program should include a time complexity analysis, in Big-Oh notation, for

your implementation for task 1, depending on the number n of words and the maximum length m of a word;
your implementation for task 2, depending on the number n of words.
Note:

You may assume that
the user input is correct (a number n ≥1 followed by n words);
the user inputs the words in alphabetical order;
no word has more than 19 characters;
there will be no more than 1000 words.
It may not be immediately obvious, but this problem is best understood and solved as a graph problem. Hence, if you find any of the following ADTs from the lectures useful, then you can, and indeed are encouraged to, use them with your program:

stack ADT :   stack.h, stack.c
queue ADT :   queue.h, queue.c
graph ADT :   Graph.h, Graph.c
weighted graph ADT :   WGraph.h, WGraph.c
You are free to modify any of the four ADTs for the purpose of the assignment (but without changing the file names). If your program is using one or more of these ADTs, you should submit both the header and implementation file, even if you have not changed them.

Your main program file should start with a comment: /* … */ that contains the time complexity of your solutions for task 1 and task 2, together with an explanation.


Stage 1 (3 marks)

For stage 1, you should demonstrate that you can build the underlying graph correctly under the assumption that all words are of equal length.

All tests for this stage will be such that all words have the same length and all given words together form a word chain. Hence, all you need to do for task 2 at this stage is to output the total number of words (= maximum length of a chain) and all words (= the only maximal chain).

Here is an example to show the desired behaviour of your program for a stage 1 test:
./wordchains
Enter a number: 6
Enter word: bear
Enter word: dear
Enter word: hear
Enter word: heat
Enter word: neat
Enter word: seat

bear: dear hear
dear: hear
hear: heat
heat: neat seat
neat: seat
seat:

Maximum chain length: 6
Maximal chains:
bear -> dear -> hear -> heat -> neat -> seat

Stage 2 (3 marks)

For stage 2, you should demonstrate that you can find a single maximal chain under the assumption that all words are of equal length.

All tests for this stage will be such that all words have the same length and there is only one maximal word chain.

Here is an example to show the desired behaviour of your program for a stage 2 test:
./wordchains
Enter a number: 8
Enter word: bear
Enter word: beer
Enter word: dear
Enter word: deer
Enter word: hear
Enter word: heat
Enter word: rear
Enter word: seat

bear: beer dear hear rear
beer: deer
dear: deer hear rear
deer:
hear: heat rear
heat: seat
rear:
seat:

Maximum chain length: 5
Maximal chains:
bear -> dear -> hear -> heat -> seat

Stage 3 (3 marks)

For stage 3, you should extend your program for stage 2 such that words can be of different length.

All tests for this stage will be such that there is only one maximal word chain.

Here is an example to show the desired behaviour of your program for a stage 3 test:
./wordchains
Enter a number: 6
Enter word: cast
Enter word: cat
Enter word: cats
Enter word: cost
Enter word: most
Enter word: moyst

cast: cat cost
cat: cats
cats:
cost: most
most: moyst
moyst:

Maximum chain length: 4
Maximal chains:
cast -> cost -> most -> moyst

Stage 4 (3 marks)

For stage 4, you should extend your program for stage 3 such that it outputs, in alphabetical order, all word chains of maximal length.

Here is an example to show the desired behaviour of your program for a stage 4 test:
./wordchains
Enter a number: 5
Enter word: cast
Enter word: cat
Enter word: cats
Enter word: cost
Enter word: most

cast: cat cost
cat: cats
cats:
cost: most
most:

Maximum chain length: 3
Maximal chains:
cast -> cat -> cats
cast -> cost -> most
Note:

It is required that the maximal chains be printed in alphabetical order.
