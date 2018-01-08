// pydll.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include <iostream>
#include <random>

#include <thread>
#include <unordered_set>
#include <vector>
using namespace std;

template<>
struct hash<pair<int, int>> {
	size_t operator()(const pair<int, int>& pt) const
	{
		return (pt.first << 16) + pt.second;
	}
};

void vector_str(vector<pair<int, int>>& path, char* line)
{
	if (!path.size())
		return;
	line[0] = '[';
	int i = 1;
	for (auto& pt : path)
	{
		line[i++] = '(';
		line[i++] = pt.first + '0';
		line[i++] = ',';
		line[i++] = ' ';
		line[i++] = pt.second + '0';
		line[i++] = ')';
		line[i++] = ',';
		line[i++] = ' ';
	}
	line[i - 2] = ']';
	line[i - 1] = 0;
}

int sumGrid(const int grid[10][10])
{
	int sum = 0;
	for (int y = 0; y < 10; y++)
		for (int x = 0; x < 10; x++)
			sum += grid[y][x];
	return sum;
}

vector<pair<int, int>> vec[4][4];
int found[4] = { 0,0,0,0 };

void seek(const pair<int, int>& root, const int grid[10][10], const int& initialDirection, const int& nextDirection, const int& target)
{
	if (abs(initialDirection - nextDirection) == 2)
		return;
	int sum = grid[root.first][root.second];
	char directions[10][10][5];
	memset(directions, 0, 500);
	vector<pair<int, int>> stack;
	unordered_set<pair<int, int>> stack_set;
	stack_set.insert(root);
	stack.push_back(root);

	pair<int, int> nxt = make_pair(-1, -1);

	if (initialDirection == 3 && root.second != 0)
	{
		nxt.first = root.first;
		nxt.second = root.second - 1;
	}
	else if (initialDirection == 2 && root.first != 9)
	{
		nxt.first = root.first + 1;
		nxt.second = root.second;
	}
	else if (initialDirection == 1 && root.second != 9)
	{
		nxt.first = root.first;
		nxt.second = root.second + 1;
	}
	else if (initialDirection == 0 && root.first != 0)
	{
		nxt.first = root.first - 1;
		nxt.second = root.second;
	}
	if (nxt.first == -1)
		return;
	sum += grid[nxt.first][nxt.second];
	stack.push_back(nxt);
	stack_set.insert(nxt);

	pair<int, int> nxt2 = make_pair(-1, -1);
	pair<int, int> *pt = &stack[stack.size() - 1];

	int direction = nextDirection;
	if (direction == 3 && pt->second != 0)
	{
		nxt2.first = pt->first;
		nxt2.second = pt->second - 1;
	}
	else if (direction == 2 && pt->first != 9)
	{
		nxt2.first = pt->first + 1;
		nxt2.second = pt->second;
	}
	else if (direction == 1 && pt->second != 9)
	{
		nxt2.first = pt->first;
		nxt2.second = pt->second + 1;
	}
	else if (direction == 0 && pt->first != 0)
	{
		nxt2.first = pt->first - 1;
		nxt2.second = pt->second;
	}
	if (nxt2.first == -1)
		return;
	int backDirection = direction + 2;
	if (backDirection > 3)
		backDirection -= 4;
	directions[nxt2.first][nxt2.second][backDirection] = 1;
	sum += grid[nxt2.first][nxt2.second];
	stack.push_back(nxt2);
	stack_set.insert(nxt2);

	do
	{
		for (int i = 0; i < initialDirection; i++)
			if (found[i])
				return;
		for (int j = 0; j < 4; j++)
		{
			int d = nextDirection + j;
			if (d > 3)
				d -= 4;
			if (vec[initialDirection][d].size())
				return;
		}

		pair<int, int> nxt = make_pair(-1, -1);
		pair<int, int> *pt = &stack[stack.size() - 1];
		if (sum < target)
		{
			for (int i = 0; i < 4; i++)
			{
				if (direction == 3 && pt->second != 0 && directions[pt->first][pt->second][direction] == 0)
				{
					nxt.first = pt->first;
					nxt.second = pt->second - 1;
					if (stack_set.find(nxt) == stack_set.end())
						break;
					else
						nxt.first = -1;
				}
				else if (direction == 2 && pt->first != 9 && directions[pt->first][pt->second][direction] == 0)
				{
					nxt.first = pt->first + 1;
					nxt.second = pt->second;
					if (stack_set.find(nxt) == stack_set.end())
						break;
					else
						nxt.first = -1;
				}
				else if (direction == 1 && pt->second != 9 && directions[pt->first][pt->second][direction] == 0)
				{
					nxt.first = pt->first;
					nxt.second = pt->second + 1;
					if (stack_set.find(nxt) == stack_set.end())
						break;
					else
						nxt.first = -1;
				}
				else if (direction == 0 && pt->first != 0 && directions[pt->first][pt->second][direction] == 0)
				{
					nxt.first = pt->first - 1;
					nxt.second = pt->second;
					if (stack_set.find(nxt) == stack_set.end())
						break;
					else
						nxt.first = -1;
				}
				direction++;
				if (direction == 4)
					direction = 0;
			}
		}
		if (nxt.first != -1)
		{
			int backDirection = direction + 2;
			if (backDirection > 3)
				backDirection -= 4;
			directions[nxt.first][nxt.second][backDirection] = 1;
			directions[pt->first][pt->second][4] = direction;
			directions[pt->first][pt->second][direction] = 1;
			stack.push_back(nxt);
			stack_set.insert(nxt);
			sum += grid[nxt.first][nxt.second];
			if (sum == target)
			{
				vec[initialDirection][nextDirection] = vector<pair<int, int>>(stack);
				found[initialDirection] = 1;
				return;
			}
		}
		else
		{
			sum -= grid[pt->first][pt->second];
			memset(&directions[pt->first][pt->second][0], 0, 5);
			stack_set.erase(*pt);
			stack.pop_back();
			if (stack.size())
				direction = directions[stack[stack.size() - 1].first][stack[stack.size() - 1].second][4];
		}
	} while (stack.size() > 2);
}


extern "C" _declspec(dllexport) void DFS(char* out, const int grid[10][10], const int& x, const int& y, const int& target)
{
	if (sumGrid(grid) < target)
		return;
	int sum = grid[x][y];
	pair<int, int> root = make_pair(x, y);
	if (sum < target)
	{
		thread th[16];
		for (int i = 0; i < 4; i++)
			for (int j = 0; j < 4; j++)
			{
				int nextdirection = i + j;
				if (nextdirection > 3)
					nextdirection -= 4;
				th[i * 4 + j] = thread(seek, root, grid, i, nextdirection, target);
			}
		for (int i = 0; i < 16; i++)
			th[i].join();
		for (int i = 0; i < 4; i++)
		{
			if (found[i])
			{
				for (int j = 0; j < 4; j++)
				{
					if (vec[i][j].size())
					{
						vector_str(vec[i][j], out);
						return;
					}
				}
			}
		}
	}
}

int main()
{
	ios::sync_with_stdio(false);
	srand(4);
	int grid[10][10] = {
		{ 1,1,0,1,1,1,1,1,1,0		},{ 0,1,0,0,1,0,1,0,0,1		},{ 1,0,1,1,1,0,1,1,1,0		},{ 0,0,1,0,1,1,0,1,0,0		},{ 0,0,0,1,0,0,1,1,0,1		},{ 1,0,1,0,1,1,0,1,1,0		},{ 1,0,0,0,0,1,1,0,0,0		},{ 0,0,0,1,1,0,0,1,1,1		},{ 1,1,0,1,0,1,1,0,0,0		},{ 1,0,0,1,0,1,1,0,0,0 }

	};
	char result[1000];
	result[0] = 0;
	DFS(result, grid, 0, 0, 50);
	cout << result << endl;
	getchar();
}


/*	{1,1,0,1,1,1,1,1,1,0
	}, { 0,1,0,0,1,0,1,0,0,1
	}, { 1,0,1,1,1,0,1,1,1,0
	}, { 0,0,1,0,1,1,0,1,0,0
	}, { 0,0,0,1,0,0,1,1,0,1
	}, { 1,0,1,0,1,1,0,1,1,0
	}, { 1,0,0,0,0,1,1,0,0,0
	}, { 0,0,0,1,1,0,0,1,1,1
	}, { 1,1,0,1,0,1,1,0,0,0
	}, { 1,0,0,1,0,1,1,0,0,0}


		{ 1,1,0,1,1,1,1,1,1,0 },
		{ 0,1,0,0,1,0,1,0,0,1 },
		{ 1,0,1,1,1,0,1,1,1,0 },
		{ 0,0,1,0,1,1,0,1,0,0 }	,
		{ 0,0,0,1,0,0,1,1,0,1 },
		{ 1,0,1,0,1,1,0,1,1,0 },
		{ 1,0,0,0,0,1,1,0,0,0 },
		{ 0,0,0,1,1,0,0,1,1,1 },
		{ 1,1,0,1,0,1,1,0,0,0 },
		{ 1,0,0,1,0,1,1,0,0,0 }

		{ 1,1,0,1,1,1,1,1,1,0 },
		{ 0,1,0,0,1,0,1,0,0,1 },
		{ 1,0,1,1,1,0,1,1,1,0 },
		{ 0,0,1,0,1,1,0,1,0,0 },
		{ 0,0,0,1,0,0,1,1,0,1 },
		{ 1,0,1,0,1,1,0,1,1,0 },
		{ 1,0,0,0,0,1,1,0,0,0 },
		{ 0,0,0,1,1,0,0,1,1,1 },
		{ 1,1,0,1,0,1,1,0,0,0 },
		{ 1,0,0,1,0,1,1,0,0,0 }

		0 2 0 0 50

		{1,1,0,1,1,1,1,1,1,0		},{0,1,0,0,1,0,1,0,0,1		},{1,0,1,1,1,0,1,1,1,0		},{0,0,1,0,1,1,0,1,0,0		},{0,0,0,1,0,0,1,1,0,1		},{1,0,1,0,1,1,0,1,1,0		},{1,0,0,0,0,1,1,0,0,0		},{0,0,0,1,1,0,0,1,1,1		},{1,1,0,1,0,1,1,0,0,0		},{1,0,0,1,0,1,1,0,0,0}

		*/