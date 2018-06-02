#include <iostream>
#include "SimpleSerial.hpp"

#define LINHAS 24   

using namespace std;
using namespace boost;

int main(int argc, char* argv[])
{
    // string message;
    // try {

    //     SimpleSerial serial("/dev/ttyACM0",9600);

    //     for(;;)
    //     {
    //         std::cout << ">>";
    //         std::cin >> message;
    //         if(message.compare("fim") == 0 )
    //             break;
            
    //         serial.writeString(message);

    //         cout<<serial.readLine()<<endl;
    //     }
        

    // } catch(boost::system::system_error& e)
    // {
    //     cout<<"Error: "<<e.what()<<endl;
    //     return 1;
    // }

//-------coletar 24 linhas de dados--------
//(D0=1 D1=0 D2=0 D3=0 A2=0 A1=0 A0=0 output) conecta j0 l0
//(D0=0 D1=1 D2=0 D3=0 A2=0 A1=0 A1=1 output) conecta j1 l1 

    int linhas[LINHAS], mensagem[LINHAS];
    int i = 0;

    std::cout << ((8-1)%4) << endl;

    std::cout << "DIGITE A CONFIGURAÇÃO DA MATRIZ (24 linhas por 12 colunas)" << endl;
    for(i=0; i<LINHAS; i++)
    {
        std::cout << "COLUNA "<< i << ":";
        std::cin >> linhas[i]; 
    }

    
}