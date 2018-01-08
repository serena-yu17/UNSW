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

typedef unsigned char byte;

struct point
{
	byte y;
	byte x;
	point(byte x0, byte y0)
	{
		x = x0;
		y = y0;
	}
	point()
	{	}
};


void dfs(size_t* count, byte x0, byte y0, unordered_map<int32_t, byte>& pow2)
{
	vector<point> stack;
	int32_t ** grid = new int32_t*[n];
	for (int i = 0; i < n; i++)
		grid[i] = new int32_t[n];
	point root = point(x0, y0);
	byte j = 1;
	memset(grid[root.y], -1, n * sizeof(int32_t));
	while (y0 + j < n)
	{
		if (x0 + j < n)
			grid[root.y][y0 + j] &= ~(1 << (x0 + j));
		if (x0 - j > -1)
			grid[root.y][y0 + j] &= ~(1 << (x0 - j));
		grid[root.y][y0 + j] &= ~(1 << x0);
		j++;
	}
	stack.push_back(root);
	while (stack.size())
	{
		point* top = &stack[stack.size() - 1];
		byte y = top->y + 1;
		if (grid[top->y][y] & ((1 << n) - 1) && stack.size() != n)
		{
			point nxt = point();
			int32_t firstPosition = grid[top->y][y] & (-grid[top->y][y]);
			const byte x = pow2[firstPosition];
			nxt.x = x;
			nxt.y = y;
			memcpy(grid[nxt.y] + y, grid[top->y] + y, (n - y) * sizeof(int32_t));
			grid[nxt.y][y] &= ~firstPosition;
			j = 1;
			while (y + j < n)
			{
				if (x + j < n)
					grid[nxt.y][y + j] &= ~(1 << (x + j));
				if (x - j > -1)
					grid[nxt.y][y + j] &= ~(1 << (x - j));
				grid[nxt.y][y + j] &= ~(1 << x);
				j++;
			}
			stack.push_back(nxt);
		}
		else {
			if (stack.size() == n)
				(*count)++;
			memset(grid[top->y] + top->y, -1, (n - top->y) * sizeof(int32_t));
			if (stack.size() > 1)
				grid[stack[stack.size() - 2].y][top->y] &= ~(1 << top->x);
			stack.pop_back();
		}
	}
	for (byte i = 0; i < n; i++)
		delete[] grid[i];
	delete[] grid;
}

const char* int2char(const int32_t& in)
{
	byte size = CHAR_BIT * sizeof(int32_t);
	char* result = new char[size + 1];
	result[size] = 0;
	byte i = size - 1;
	int32_t n = in;
	while (i > -1)
	{
		result[i--] = (n & 1) + '0';
		n >>= 1;
	}
	return result;
}


size_t queens()
{
	unordered_map<int32_t, byte> pow2;
	for (byte i = 0; i < n; i++)
		pow2[1 << i] = i;
	size_t* countThread = new size_t[n]();
	size_t count = 0;
	vector<thread> th;
	for (byte x = 0; x < n; x++)
		th.push_back(thread(dfs, countThread + x, x, 0, pow2));
	for (byte x = 0; x < n; x++)
	{
		th[x].join();
		count += countThread[x];
	}
	delete countThread;
	return count;
}


int main()
{
	ios::sync_with_stdio(false);
	while (1)
	{
		cout << "Enter number of queens:" << endl;
		cin >> n;
		if (n > 30)
		{
			cout << "Input is too large too handle.\n" << endl;
			continue;
		}
		auto start = chrono::steady_clock::now();
		size_t result = queens();
		auto duration = chrono::duration_cast<std::chrono::milliseconds>(chrono::steady_clock::now() - start);
		cout << "Time elapsed: " << duration.count() << "ms" << endl;
		cout << "Number of solutions: " << result << "\n" << endl;
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

