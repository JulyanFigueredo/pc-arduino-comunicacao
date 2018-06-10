#include <iostream>
#include "SimpleSerial.hpp"
#include <bitset>

#define LINHAS 8 //nº de linhas de cada placa
#define COLUNAS 4 //nº de colunas de cada placa
#define LINHAS_MATRIZ 24 //nº de linhas de cada placa
#define COLUNAS_MATRIZ 12 //nº de colunas de cada placa
#define PLACAS 9
#define ORDEM 3//ordem da matriz de interconexões

using namespace std;
using namespace boost;

int coluna[LINHAS_MATRIZ], mensagem[LINHAS][PLACAS], pilha=0, linha_da_placa=0, 
    coluna_da_placa=0, n_placa=0;

void ConfigurarMatriz()
{
    
    //o vetor coluna[] recebe 24 valores para as 24 linhas da matriz desse sistema
    int i=0, j=0;

    for(i=0; i<LINHAS; i++)
    {
        for(j=0; j<PLACAS; j++)
        {
            mensagem[i][j] = i << 1;
            //std::cout << ">>"<< bitset<8>(mensagem[i][j]) << endl;    
        }
        
    }

    std::cout << "DIGITE A CONFIGURAÇÃO DA MATRIZ (24 linhas por 12 colunas)" << endl;
    for(i=0; i<LINHAS_MATRIZ; i++)
    {
        std::cout << "LINHA "<< std::dec << i << ", COLUNA:";
        std::cin >> coluna[i]; //de 0 a 11, tem 12 colunas
        
        //tendo a linha(i), descobrir em qual pilha(0, 1 ou 2) de placas está essa linha
        pilha = i/LINHAS;
        std::cout << "pilha: "<< pilha << endl;

        //descobrir a linha da placa, usado na matriz de bytes
        linha_da_placa = i%LINHAS;
        std::cout << "linha da placa: "<< linha_da_placa << endl;

        //descobrir a coluna da placa, usado na matriz de bytes
        coluna_da_placa = coluna[i]%COLUNAS;
        std::cout << "coluna da placa: "<< coluna_da_placa << endl;

        //descobrir o nº da placa(de 0 a 8)
        n_placa = pilha*ORDEM + coluna[i]/4;
        std::cout << "número placa :"<< n_placa << endl;

        mensagem[linha_da_placa][n_placa] |= (1 << (7-coluna_da_placa)); 
        std::cout << ">>"<< bitset<8>(mensagem[linha_da_placa][n_placa]) << endl;  
        std::cout << ">>"<< std::hex << std::uppercase << mensagem[linha_da_placa][n_placa] << endl; 
    }
}


int main(int argc, char* argv[])
{
    try {

        SimpleSerial serial("/dev/ttyACM1",9600);
        std::cout << "Abriu a porta serial" << endl;
        //ConfigurarMatriz();

        int i,j;
        unsigned char m;
        m = 'a';
        for(i=0; i<LINHAS; i++)
        {
            for(j=0; j<PLACAS; j++)
            {
                std::cout << "entrou no for" << endl;
                //std::cout << ">>"<< std::hex << mensagem[i][j] << "
                serial.writeString(m);
                //serial.writeString(m);
                std::cout << serial.readLine() << endl;
                //serial.writeString((char*)mensagem[i][j]);
            }
            std::cout << " "<< endl;

        }

    } catch(boost::system::system_error& e)
    {
        cout<<"Error: "<<e.what()<<endl;
        return 1;
    }

// tendo essa grande matriz de bytes que configura a matriz de interconexões, temos que enviar pela serial

    // string message;
    // try {

    //     SimpleSerial serial("/dev/ttyACM0",9600);

    //     for(;;)
    //     {
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

//cada placa vai ter um vetor de 8 posições, farei então uma matriz de 8 linhas por 9 placas
//Em cada placa, cada linha pode se conectar a qualquer coluna. Porém, neste sistema, é necessário
//que cada coluna receba qualquer linha, mas cada linha deve se conectar à uma só coluna. Isso vem do 
//fato de que em um circuito elétrico, cada terminal de componente pode ser conectado à um unico nó. 

}