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

bool cmp(const pair<int, int> &left, const pair<int, int> &right)
{
	return left.first < right.first || (left.first == right.first && left.second < right.second);
}

string solution(int n, int t, int m, vector<string> timetable) 
{
	string answer = "";

	vector<pair<int, int> > bus;
	int hour = 9, minute = 0;
	for (int i = 0; i < n; i++)
	{
		bus.push_back(make_pair(hour, minute));
		minute += t;
		hour += minute / 60;
		minute %= 60;
	}

	vector<pair<int, int> > vt;
	for (int i = 0; i < timetable.size(); i++)
	{
		hour = (int)(timetable[i][0] - '0') * 10 + (int)(timetable[i][1] - '0');
		minute = (int)(timetable[i][3] - '0') * 10 + (int)(timetable[i][4] - '0');
		vt.push_back(make_pair(hour, minute));
	}
	sort(vt.begin(), vt.end(), cmp);

	int pos = 0, conH = 0, conM = 0, lastH, lastM, temp;
	for (int i = 0; i < bus.size(); i++)
	{
		temp = m;

		cout << "bus : " << bus[i].first << " " << bus[i].second << endl;
		for (; pos < vt.size() && (vt[pos].first < bus[i].first || (vt[pos].first == bus[i].first && vt[pos].second <= bus[i].second)); pos++)
		{
			if (temp == 0)
				break;

			cout << "crew : " << vt[pos].first << " " << vt[pos].second << endl;
			lastH = vt[pos].first; lastM = vt[pos].second;
			temp--;
		}

		if (temp != 0)
		{
			conH = bus[i].first;
			conM = bus[i].second;
		}
		else
		{
			conH = lastH;
			conM = lastM - 1;
			if (conM < 0)
			{
				conH--;
				conM = 59;
			}
		}		
	}
	
	answer += ((char)((conH / 10) + '0'));
	answer += ((char)((conH % 10) + '0'));
	answer += ":";
	answer += ((char)((conM / 10) + '0'));
	answer += ((char)((conM % 10) + '0'));

	return answer;
}