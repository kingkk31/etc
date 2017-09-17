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

int solution(string dartResult) {
    int answer = 0;

	vector<int> vt;
	stack<int> st;

	for (int i = 0; i < dartResult.length(); i++)
	{
		if (dartResult[i] == 'S' || dartResult[i] == 'D' || dartResult[i] == 'T')
		{
			int val = 0, p = 0;
			while (!st.empty())
			{
				val += (st.top() * pow(10, p++));
				st.pop();
			}

			switch (dartResult[i])
			{
			case 'D': val = val * val; break;
			case 'T': val = val * val * val; break;
			}

			vt.push_back(val);

		}
		else if (dartResult[i] == '*' || dartResult[i] == '#')
		{
			if (dartResult[i] == '#')
				vt.back() *= -1;
			else
			{
				if (vt.size() > 1)
					vt[vt.size() - 2] *= 2;
				
				vt[vt.size() - 1] *= 2;
			}
		}
		else
			st.push((int)(dartResult[i] - '0'));
	}
	
	for (int i = 0; i < vt.size(); i++)
		answer += vt[i];
	
	return answer;
}