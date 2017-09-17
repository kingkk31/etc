#include <string>
#include <vector>

using namespace std;

vector<string> solution(int n, vector<int> arr1, vector<int> arr2) {
    vector<string> answer;

	for (int i = 0; i < n; i++)
	{
		string row1 = "", row2 = "";
		int temp1 = arr1[i], temp2 = arr2[i];
		for (int j = 0; j < n; j++)
		{
			if (temp1 % 2 == 1)
				row1 = "1" + row1;
			else
				row1 = "0" + row1;
			temp1 /= 2;

			if (temp2 % 2 == 1)
				row2 = "1" + row2;
			else
				row2 = "0" + row2;
			temp2 /= 2;
		}
		
		string ans = "";
		for (int j = 0; j < n; j++)
		{
			if (row1[j] == '0' && row2[j] == '0')
				ans = ans + " ";
			else
				ans = ans + "#";
		}
		
		answer.push_back(ans);
	}
	
	return answer;
}