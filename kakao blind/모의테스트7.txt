#include <string>
#include <vector>
#include <string.h>
using namespace std;

#define INF 987654321

int cache[20001][101];
string target;

int DPSol(vector<string>& strs, int pos, int arrPos) 
{
	if (pos == target.size())
		return 0;
	
	int& ret = cache[pos][arrPos];
	if (ret != -1) 
		return ret;
	ret = INF;

	for (int i = 0; i< strs.size(); i++) 
	{
		int j = 0;

		for (; j < strs[i].size(); j++)
			if (pos + j >= target.size() || target[pos + j] != strs[i][j])
				break;

		if (j == strs[i].size())
			ret = min(ret, DPSol(strs, pos + j, i) + 1);
	}

	return ret;
}

int solution(vector<string> strs, string t)
{
	int answer = INF;
	target = t;

	memset(cache, -1, sizeof(cache));

	for (int i = 0; i < strs.size(); i++)
		answer = min(answer, DPSol(strs, 0, i));

	return  (answer == INF ? -1 : answer);
}
