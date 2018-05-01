#include <iostream>
#include "SimpleSerial.hpp"

using namespace std;
using namespace boost;

int main(int argc, char* argv[])
{
    try {

        SimpleSerial serial("/dev/ttyACM0",9600);

        serial.writeString("g\n");

        cout<<serial.readLine()<<endl;

    } catch(boost::system::system_error& e)
    {
        cout<<"Error: "<<e.what()<<endl;
        return 1;
    }
}