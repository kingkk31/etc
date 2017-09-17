#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <queue>
#include <vector>
#include <stack>
#include <set>
#include <map>
#include <list>
#include <string>
#include <string.h>
#include <math.h>
#include <algorithm>
#include <malloc.h>
#include <functional>
#include <time.h>
#include <cctype>
#pragma warning(disable:4996)
using namespace std;

int cache[100001][5];

int solve(int y, int x, vector<vector<int> > &vt)
{
	if (y >= vt.size())
		return 0;

	int &ret = cache[y][x];
	if (ret != -1)
		return ret;
	ret = 0;

	for (int i = 0; i < 4; i++)
	{
		if (i == x)
			continue;
		ret = max(ret, vt[y][x] + solve(y + 1, i, vt));
	}

	return ret;
}

int solution(vector<vector<int> > land)
{
	int answer = 0, n = land.size(), m = 4;
	for (int i = 0; i < 4; i++)
	{
		memset(cache, -1, sizeof(cache));
		answer = max(answer, solve(0, i, land));
	}

	return answer;
}

int main(void)
{
	int n, m = 4;
	vector<vector<int> > vt;

	scanf("%d", &n);
	vt = vector<vector<int> >(n, vector<int>(m));

	for (int i = 0; i < n; i++)
		for (int j = 0; j < m; j++)
			scanf("%d", &vt[i][j]);

	cout << solution(vt) << endl;

	return 0;
}