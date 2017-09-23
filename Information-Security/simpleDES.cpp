#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <string.h>
#include <algorithm>
#include <functional>
#include <bitset>
using namespace std;

int P10_table[] = { 2, 4, 1, 6, 3, 9, 0, 8, 7, 5 };
int P8_table[] = { 5, 2, 6, 3, 7, 4, 9, 8 };
int P4_table[] = { 1, 3, 2, 0 };
int IPtable[] = { 1, 5, 2, 0, 3, 7, 4, 6 };
int IP_1table[] = { 3, 0, 2, 4, 6, 1, 7, 5 };
int EPtable[] = { 3, 0, 1, 2, 1, 2, 3, 0 };
string S0box[4][4] = { {"01", "00", "11", "10"}
					,{"11", "10", "01", "00"}
					,{"00", "10", "01", "11"}
					,{ "11", "01", "11", "10" } };
string S1box[4][4] = { { "00", "01", "10", "11" }
					,{ "10", "00", "01", "11" }
					,{ "11", "00", "01", "00" }
					,{ "10", "01", "00", "10" } };

string P10(string key)
{
	string ans = "";
	for (int i = 0; i < 10; i++)
		ans += key[P10_table[i]];
	return ans;
}

string P8(string key)
{
	string ans = "";
	for (int i = 0; i < 8; i++)
		ans += key[P8_table[i]];
	return ans;
}

string P4(string key)
{
	string ans = "";
	for (int i = 0; i < 4; i++)
		ans += key[P4_table[i]];
	return ans;
}

string LS1(string key)
{
	return key.substr(1, 10) + key[0];
}

string LS2(string key)
{
	return key.substr(2, 10) + key[0] + key[1];
}

string IP(bitset<8> input)
{
	string ans = "";
	for (int i = 0; i < 8; i++)
		ans += (input.test(7 - IPtable[i]) ? "1" : "0");
	return ans;
}

bitset<8> IP_1(string input)
{
	bitset<8> ans;
	for (int i = 0; i < 8; i++)
	{
		if (input[IP_1table[i]] == '1')
			ans.set(7 - i, true);
		else
			ans.set(7 - i, false);
	}
	return ans;
}

string EP(string str)
{
	string ans = "";
	for (int i = 0; i < 8; i++)
		ans += str[EPtable[i]];
	return ans;
}

string XOR(string str, string key)
{
	string ans = "";
	for (int i = 0; i < str.length(); i++)
		ans += (str[i] == key[i] ? "0" : "1");
	return ans;
}

string Sbox(string str, int box)
{
	int row = 2 * (str[0] == '1' ? 1 : 0) + (str[3] == '1' ? 1 : 0);
	int col = 2 * (str[1] == '1' ? 1 : 0) + (str[2] == '1' ? 1 : 0);
	
	if (box == 0)
		return S0box[row][col];
	else
		return S1box[row][col];
}

string encrypt(string message, string key1, string key2)
{
	string encStr = "";
	
	for (int i = 0; i < message.length(); i++)
	{
		int plain = (int)message[i];
		bitset<8> bin_x(plain);
		string en_x = IP(bin_x);

		string left = en_x.substr(0, 4), right = en_x.substr(4, 8);
		string epXor = XOR(EP(right), key1);
		string rightF = P4(Sbox(epXor.substr(0, 4), 0) + Sbox(epXor.substr(4, 8), 1));
		string finalS = XOR(left, rightF);

		left = right, right = finalS;
		epXor = XOR(EP(right), key2);
		rightF = P4(Sbox(epXor.substr(0, 4), 0) + Sbox(epXor.substr(4, 8), 1));
		finalS = XOR(left, rightF);

		bitset<8> ans = IP_1(finalS + right);
		int cipher = ans.to_ulong();
		encStr.push_back((char)cipher);
	}

	return encStr;
}

string decrypt(string message, string key1, string key2)
{
	string decStr = "";

	for (int i = 0; i < message.length(); i++)
	{
		int plain = (int)message[i];
		bitset<8> bin_x(plain);
		string en_x = IP(bin_x);
		string left = en_x.substr(0, 4), right = en_x.substr(4, 8);
		string epXor = XOR(EP(right), key2);
		string rightF = P4(Sbox(epXor.substr(0, 4), 0) + Sbox(epXor.substr(4, 8), 1));
		string finalS = XOR(left, rightF);

		left = right, right = finalS;
		epXor = XOR(EP(right), key1);
		rightF = P4(Sbox(epXor.substr(0, 4), 0) + Sbox(epXor.substr(4, 8), 1));
		finalS = XOR(left, rightF);

		bitset<8> ans = IP_1(finalS + right);
		int cipher = ans.to_ulong();
		decStr.push_back((char)cipher);
	}

	return decStr;
}


int main(int argc, char *argv[])
{
	string key = "1010000010";
	string message(argv[1]);
	
	//******gen key******
	string temp = P10(key);
	temp = (LS1(temp.substr(0, 5)) + LS1(temp.substr(5, 10)));
	string k1 = P8(temp), k2 = P8((LS2(temp.substr(0, 5)) + LS2(temp.substr(5, 10))));
	
	string en = encrypt(message, k1, k2);
	string de = decrypt(en, k1, k2);
	cout << en << " " << de << endl;
	
	return 0;
}
