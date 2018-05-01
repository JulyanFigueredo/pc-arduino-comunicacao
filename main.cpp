#include <iostream>
#include "SimpleSerial.hpp"

using namespace std;
using namespace boost;

int main(int argc, char* argv[])
{
    string message;
    try {

        SimpleSerial serial("/dev/ttyACM0",9600);

        for(;;)
        {
            std::cout << ">>";
            std::cin >> message;
            if(message.compare("fim") == 0 )
                break;
            
            serial.writeString(message);

            cout<<serial.readLine()<<endl;
        }
        

    } catch(boost::system::system_error& e)
    {
        cout<<"Error: "<<e.what()<<endl;
        return 1;
    }
}