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

int solution(int cacheSize, vector<string> cities) 
{
	int answer = 0;
	if (cacheSize == 0)
		return answer = cities.size() * 5;

	for (int i = 0; i < cities.size(); i++)
		transform(cities[i].begin(), cities[i].end(), cities[i].begin(), ::toupper);

	vector<pair<string, int> > vt(cacheSize);
	for (int j = 0; j < cacheSize; j++)
		vt[j] = make_pair("", cacheSize - j);

	for (int i = 0; i < cities.size(); i++)
	{
		int p = -1;
		for (int j = 0; j < cacheSize; j++)
		{
			if (vt[j].first == cities[i])
			{
				p = j;
				break;
			}
		}
		
		if (p != -1)
		{
			answer += 1;
			vt[p].second = 0;
		}
		else
		{
			answer += 5;

			int pos = 0, maxi = -1;
			for (int j = 0; j < cacheSize; j++)
			{
				if (vt[j].second > maxi)
				{
					pos = j;
					maxi = vt[j].second;
				}
			}

			vt[pos] = make_pair(cities[i], 0);
		}
		
		for (int j = 0; j < cacheSize; j++)
			vt[j].second += 1;
	}

	return answer;
}