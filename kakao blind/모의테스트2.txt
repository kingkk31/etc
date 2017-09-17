#include<vector>
#include <iostream>
#include <stdio.h>
using namespace std;

bool solution(vector<int> arr)
{
	bool answer = true;
    vector<bool> check(arr.size()+1, false);
    
    for(int i=0;i<arr.size();i++)
    {
        int num = arr[i];
        if(check[num])
        {
            answer = false;
            break;
        }
        check[num] = true;
    }
    
    for(int i=1;i<=arr.size();i++)
        if(!check[i])
        {
            answer = false;
            break;
        }
    
	return answer;
}