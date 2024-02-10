#include <string.h>
#include <string>
#include <iostream>

using namespace std;

int main() {
	Serial* SP = new Serial("\\\\.\\COM3");
	if (SP->IsConnected())
	{
		cout << "We're connected" << endl;
		cout << "________________" << endl;
	}

	char incomingData[256] = "";
	int readResult = 0;

	while (SP->IsConnected())
	{
		readResult = SP->ReadData(incomingData);
		incomingData[readResult] = 0;

		if (strlen(incomingData) > 0) 
		{
			string str(incomingData);
			cout << endl << "String: " << str << endl;

			for (int i = 0; i < strlen(incomingData); i++)
			{
				cout << "Char on place " << i << ": " << incomingData[i] << endl;
			}
			cout <<     "________________" << endl;
		}
	}
}