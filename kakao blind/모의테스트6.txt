#include <vector>
#include <string.h>
using namespace std;

int cache[100001][2];

int solve(int pos, vector<int> &vt, bool flag)
{
	if (pos >= vt.size())
		return 0;
	if (pos == (vt.size() - 1)) 
	{
		if (flag)
			return 0;
		return vt[pos];
	}

	int &ret = cache[pos][(int)flag];
	if (ret != -1)
		return ret;
	ret = 0;

	ret = max(ret, max(solve(pos + 3, vt, flag) + vt[pos], solve(pos + 2, vt, flag) + vt[pos]));
	return ret;
}

int solution(vector<int> sticker)
{
	int answer = 0;
	if(sticker.size() == 1)
		return answer = sticker[0];

	memset(cache, -1, sizeof(cache));
	answer = max(answer, max(solve(0, sticker, true), max(solve(1, sticker, false), solve(2, sticker, false))));

	return answer;
}
