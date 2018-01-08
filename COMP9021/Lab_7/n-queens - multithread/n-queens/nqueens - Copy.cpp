// nqueens.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <vector>
#include <chrono>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <thread>
using namespace std;

int n;


class point
{
public:
	int y;
	int x;
	int64_t* grid = new int64_t[n];
	point(int x0, int y0)
	{
		x = x0;
		y = y0;
		memset(grid, -1, n * sizeof(int64_t));
	}
	point(point* pt, int y)
	{
		memcpy(grid + y, pt->grid + y, sizeof(int64_t)*(n - y));
	}
	bool operator==(point& other)
	{
		return x == other.x && y == other.y;
	}
	bool operator!=(point& other)
	{
		return !(*this == other);
	}
	~point()
	{
		delete grid;
	}
};

template<>
struct hash<point*>
{
	size_t operator()(const point* pt) const
	{
		return (pt->x) << 16 + pt->y;
	}
};


void dfs(vector<int*>* result, int x0, int y0, unordered_map<int64_t, int>& pow2)
{
	vector<point*> stack;
	point* root = new point(x0, y0);
	int j = 1;
	while (y0 + j < n)
	{
		if (x0 + j < n)
			root->grid[y0 + j] &= ~(1 << (x0 + j));
		if (x0 - j > -1)
			root->grid[y0 + j] &= ~(1 << (x0 - j));
		root->grid[y0 + j] &= ~(1 << x0);
		j++;
	}
	stack.push_back(root);
	while (stack.size())
	{

		point* top = stack[stack.size() - 1];
		point* nxt = NULL;
		int y = top->y + 1;
		if (stack.size() == n)
		{
			int* res = new int[n];
			for (int i = 0; i < n; i++)
				res[i] = stack[i]->x;
			result->push_back(res);
		}
		else if (top->grid[y] & ((1 << n) - 1))
		{
			nxt = new point(top, y);
			int64_t firstPosition = top->grid[y] & (-top->grid[y]);
			const int x = pow2[firstPosition];
			nxt->x = x;
			nxt->y = y;
			nxt->grid[y] &= ~firstPosition;
			j = 1;
			while (y + j < n)
			{
				if (x + j < n)
					nxt->grid[y + j] &= ~(1 << (x + j));
				if (x - j > -1)
					nxt->grid[y + j] &= ~(1 << (x - j));
				nxt->grid[y + j] &= ~(1 << x);
				j++;
			}
			stack.push_back(nxt);
		}
		if (!nxt)
		{
			stack.pop_back();
			if (stack.size())
				stack[stack.size() - 1]->grid[top->y] &= ~(1 << top->x);
			delete top;
		}
	}
}

const char* int2char(const int64_t& in)
{
	int size = CHAR_BIT * sizeof(int64_t);
	char* result = new char[size + 1];
	result[size] = 0;
	int i = size - 1;
	int64_t n = in;
	while (i > -1)
	{
		result[i--] = (n & 1) + '0';
		n >>= 1;
	}
	return result;
}

int64_t power(int base, int n)
{
	if (!base && n)
		return 0;
	int64_t pow = 1;
	while (n) {
		if (n & 1)
			pow *= base;
		base *= base;
		n >>= 1;
	}
	return pow;
}


vector<int*>* queens()
{
	unordered_map<int64_t, int> pow2;
	for (int i = 0; i < 63; i++)
		pow2[power(2, i)] = i;
	vector<int*>** searchResult = new vector<int*>*[n]();
	vector<int*>* result = new vector<int*>();
	vector<thread> th;
	for (int x = 0; x < n; x++)
	{
		searchResult[x] = new vector<int*>();
		th.push_back(thread(dfs, searchResult[x], x, 0, pow2));
	}
	for (int x = 0; x < n; x++)
	{
		th[x].join();
		for (int* comb : *searchResult[x])
			result->push_back(comb);
		delete searchResult[x];
	}
	delete searchResult;
	return result;
}


int main()
{
	ios::sync_with_stdio(false);
	while (1)
	{
		cout << "Enter number of queens:" << endl;
		cin >> n;
		if (n > 62)
		{
			cout << "Input too large too handle.\n" << endl;
			continue;
		}
		auto start = chrono::steady_clock::now();
		vector<int*>* result = queens();
		auto duration = chrono::duration_cast<std::chrono::milliseconds>(chrono::steady_clock::now() - start);
		cout << "Time elapsed: " << duration.count() << "ms" << endl;
		cout << "Number of solutions: " << result->size() << "\n" << endl;
		for (int* comb : *result)
			delete comb;
		delete result;
		/*cout << "Print number of solution:" << endl;
		int nSolution;
		cin >> nSolution;
		int* line = (*result)[nSolution];
		for (int i = 0; i < n; i++)
		cout << line[i];
		cout << endl;*/
	}
	return 0;
}

