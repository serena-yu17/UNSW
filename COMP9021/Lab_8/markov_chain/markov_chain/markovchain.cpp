// markovchain.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <string>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <random>
#include <chrono>
using namespace std;

void readFile(unordered_set<string>*);
vector<string>* markov(int, int, unordered_map<string, vector<char>>*);
void print(vector<string>*, unordered_set<string>*);
void parse(int, unordered_map<string, vector<char>>*, unordered_set<string>*);

int main()
{
	ios::sync_with_stdio(false);
	unordered_map<string, vector<char>>* prefix = new unordered_map<string, vector<char>>();
	unordered_set<string>* dict = new unordered_set<string>();
	readFile(dict);
	while (1) {
		int depth = 0, num = 0;
		cout << "What n to use to let an n-gram determine the next character? " << endl;
		cin >> depth;
		cout << "How many words do you want to generate? " << endl;
		cin >> num;
		auto start = chrono::high_resolution_clock::now();
		if (depth < 0 || num <= 0)
			continue;
		parse(depth, prefix, dict);
		if (!prefix->size())
			continue;
		vector<string>* list = markov(num, depth, prefix);
		print(list, dict);
		chrono::duration<double> elapsed = chrono::high_resolution_clock::now() - start;
		cout << "Time elapsed: " << elapsed.count() << "\n" << endl;
		prefix->clear();
	}
	delete prefix;
	delete dict;
}

void print(vector<string>* list, unordered_set<string>* dict)
{
	for (string& str : (*list))
	{
		if (dict->find(str) == dict->end())
			cout << "Invented " << str << "\n";
		else
			cout << "Rediscovered " << str << "\n";
	}
	cout << endl;
}

vector<string>* markov(int num, int depth, unordered_map<string, vector<char>>* prefix)
{
	vector<string>* comb = new vector<string>();
	random_device rd;
	mt19937 mtRand(rd());
	int count = 0;
	uniform_int_distribution<unsigned long long> dist;
	while (count < num)
	{
		char str[1024];
		string pref = string(depth, 0);
		int len = 0;
		while (!len || str[len - 1])
		{
			if (len)
				for (int j = len - 1; j >= len - depth && j >= 0; j--)
					pref[depth - len + j] = str[j];
			vector<char>* next = &(*prefix)[pref];
			dist = uniform_int_distribution<unsigned long long>(0, next->size() - 1);
			str[len++] = (*next)[dist(mtRand)];
			str[len] = 0;
			//pref reset to '\0'
			for (int j = 0; j < depth; j++)
				pref[j] = 0;
		}
		(*comb).push_back(string(str));
		count++;
	}
	return comb;
}


void readFile(unordered_set<string>* dict)
{
	FILE* f = fopen("./dictionary.txt", "r");
	if (!f) {
		cerr << "File not found.\n" << endl;
		getchar();
		return;
	}
	char line[1024];
	while (fgets(line, 1024, f))
	{
		int len = strlen(line);
		if (line[len - 1] == '\n')
		{
			line[len - 1] = 0;
			len--;
		}
		if (len)
		{
			dict->insert(string(line));
		}


	}
	fclose(f);
}

void parse(int depth, unordered_map<string, vector<char>>* prefix, unordered_set<string>* dict)
{
	string buffer = string(depth, 0);
	for (auto& line : (*dict))
	{
		int len = line.size();
		for (int i = 0; i <= len; i++)
		{
			if (i)
				for (int j = i - 1; j >= i - depth && j >= 0; j--)
					buffer[depth - i + j] = line[j];
			if (prefix->find(buffer) == prefix->end())
				(*prefix)[buffer] = vector<char>();
			(*prefix)[buffer].push_back(line[i]);
			for (int j = 0; j < depth; j++)
				buffer[j] = 0;
		}
	}
}

