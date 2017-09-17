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
#pragma warning(disable:4996)
using namespace std;

int maxi;
int cache[1001][1001];

int solve(int y, int x, vector<vector<int> > vt)
{
	if ((y < 0 || x < 0))
		return 0;

	int &ret = cache[y][x];
	if (ret != -1)
		return ret;
	ret = 0;

	int a, b, c;
	a = solve(y - 1, x - 1, vt);
	b = solve(y, x - 1, vt);
	c = solve(y - 1, x, vt);

	if (vt[y][x] == 0)
		ret = 0;
	else if (a == 0 || b == 0 || c == 0)
		ret = 1;
	else
	{
		if (a == b && b == c)
			ret = a + 1;
		else
			ret = min(a, min(b, c)) + 1;
	}

	maxi = max(maxi, ret);

	return ret;
}

int solution(vector<vector<int> > board)
{
	maxi = 0;
	memset(cache, -1, sizeof(cache));
	int n = board.size(), m = board[0].size();

	int answer = 1234;
	solve(n - 1, m - 1, board);
	answer = maxi * maxi;
	return answer;
}

int main(void)
{
	int n, m;
	vector<vector<int> > vt;

	scanf("%d %d", &n, &m);
	vt = vector<vector<int> >(n, vector<int>(m));

	for (int i = 0; i < n; i++)
		for (int j = 0; j < m; j++)
			scanf("%d", &vt[i][j]);

	cout << solution(vt) << endl;

	return 0;
}