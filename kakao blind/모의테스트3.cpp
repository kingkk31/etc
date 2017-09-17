#include <iostream>
#include <stdio.h>
#include <map>
#include <vector>
using namespace std;

vector<int> solution(vector<vector<int> > v) {
    map<int, int> mx, my;
    for(int i=0;i<3;i++)
    {
        if(mx.count(v[i][0]))
            mx[v[i][0]] = 2;
        else
            mx[v[i][0]] = 1;
    
        if(my.count(v[i][1]))
            my[v[i][1]] = 2;
        else
            my[v[i][1]] = 1;
    }
    
    vector<int> ans;
       
    map<int,int>::iterator itr = mx.begin();
    while(itr != mx.end())
    {
        if((*itr).second == 1)
            ans.push_back((*itr).first);
        itr++;
    }
    
    itr = my.begin();
    while(itr != my.end())
    {
        if((*itr).second == 1)
            ans.push_back((*itr).first);
        itr++;
    }
        
    return ans;
}