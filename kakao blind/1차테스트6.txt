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
using namespace std;

#define INF 987654321

int solution(int m, int n, vector<string> board) 
{
	int answer = 0;
	int visited[30][30]; //없어지는 거 확인용
	bool flag;

	vector<vector<char> > vt(m, vector<char>(n));
	for (int i = 0; i < m; i++)
		for (int j = 0; j < n; j++)
			vt[i][j] = board[i][j];

	while (true)
	{
		flag = false;
		memset(visited, -1, sizeof(visited));

		for (int i = 0; i < m - 1; i++)
		{
			for (int j = 0; j < n - 1; j++)
			{
				if (vt[i][j] == '0')
					continue;

				if (vt[i][j] == vt[i][j + 1] && vt[i][j] == vt[i + 1][j] && vt[i][j] == vt[i + 1][j + 1])
				{
					flag = true;
					answer += (visited[i][j] == -1 ? 1 : 0);
					visited[i][j] = 1;
					answer += (visited[i][j + 1] == -1 ? 1 : 0);
					visited[i][j + 1] = 1;
					answer += (visited[i + 1][j] == -1 ? 1 : 0);
					visited[i + 1][j] = 1;
					answer += (visited[i + 1][j + 1] == -1 ? 1 : 0);
					visited[i + 1][j + 1] = 1;
				}
			}
		}
		//삭제블럭 확인

		vector<vector<char> > temp(m, vector<char>(n));
		for (int i = 0; i < n; i++)
		{
			int pos = m - 1;
			for (int j = m - 1; j >= 0; j--)
			{
				if (visited[j][i] == -1)
					temp[pos--][i] = vt[j][i];
			}

			for (; pos >= 0; pos--)
				temp[pos][i] = '0';
		}
		vt = temp;
		
		if (!flag)
			break;
	}

	return answer;
}