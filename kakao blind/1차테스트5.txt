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

int solution(string str1, string str2) {
	int answer = 0;

	transform(str1.begin(), str1.end(), str1.begin(), ::toupper);
	transform(str2.begin(), str2.end(), str2.begin(), ::toupper);

	map<string, int> vt1, vt2;
	string temp = "";
	for (int i = 0; i < str1.length() - 1; i++)
	{
		if ('A' <= str1[i] && str1[i] <= 'Z' && 'A' <= str1[i + 1] && str1[i + 1] <= 'Z')
		{
			temp += str1[i];
			temp += str1[i + 1];
	
			if (vt1.find(temp) != vt1.end())
				vt1[temp]++;
			else
				vt1[temp] = 1;
			
			temp = "";
		}
	}
	for (int i = 0; i < str2.length() - 1; i++)
	{
		if ('A' <= str2[i] && str2[i] <= 'Z' && 'A' <= str2[i + 1] && str2[i + 1] <= 'Z')
		{
			temp += str2[i];
			temp += str2[i + 1];
			
			if (vt2.find(temp) != vt2.end())
				vt2[temp]++;
			else
				vt2[temp] = 1;
			temp = "";
		}
	}

	int a = 0, b = 0;

	map<string, int>::iterator itr = vt1.begin();
	while (itr != vt1.end())
	{
		if (vt2.find((*itr).first) == vt2.end())
		{
			b += (*itr).second;
		}
		else
		{
			a += min(vt1[(*itr).first], vt2[(*itr).first]);
			b += max(vt1[(*itr).first], vt2[(*itr).first]);
		}
		itr++;
	}

	itr = vt2.begin();
	while (itr != vt2.end())
	{
		if (vt1.find((*itr).first) == vt1.end())
			b += (*itr).second;
		itr++;
	}
	
	if (a == 0 && b == 0)
		return 65536;

	return answer = a * 65536 / b;
}