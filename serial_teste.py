# This Python file uses the following encoding: utf-8

import serial
import numpy

ser = serial.Serial(port='/dev/ttyACM1', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=2) 
try:
    ser.isOpen()
    print("Conexão serial aberta")
except:
    print("Erro")
    exit()

# if(ser.isOpen):
#     try:
#         while(1):
#             print(ser.read())
#     except Exception:
#             print("erro")
# else:
#     ("A porta serial não abre")       

LINHAS = 8 
COLUNAS = 4
LINHAS_MATRIZ = 24
COLUNAS_MATRIZ = 12 
PLACAS = 9
ORDEM = 3 

# mensagem = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'),bytearray(b'\x02\x02\x02\x02\x02\x02\x02\x02\x02'),bytearray(b'\x04\x04\x04\x04\x04\x04\x04\x04\x04'),bytearray(b'\x06\x06\x06\x06\x06\x06\x06\x06\x06'),bytearray(b'\x08\x08\x08\x08\x08\x08\x08\x08\x08'),bytearray(b'\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a\x0a'),bytearray(b'\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C'),bytearray(b'\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E') 

def LimparMatriz():
    mensagem = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'),bytearray(b'\x02\x02\x02\x02\x02\x02\x02\x02\x02'),bytearray(b'\x04\x04\x04\x04\x04\x04\x04\x04\x04'),bytearray(b'\x06\x06\x06\x06\x06\x06\x06\x06\x06'),bytearray(b'\x08\x08\x08\x08\x08\x08\x08\x08\x08'),bytearray(b'\x0A\x0A\x0A\x0A\x0A\x0A\x0A\x0A\x0A'),bytearray(b'\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C'),bytearray(b'\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E')
    print(mensagem)
    return mensagem

def ConfigurarMatriz(mensagem):
    # o vetor coluna[] recebe 24 valores para as 24 linhas da matriz desse sistema
    i=0
    j=0
    print(mensagem)
    print('DIGITE A CONFIGURAÇÃO DA MATRIZ (24 linhas por 12 colunas)');
    for i in xrange (0, LINHAS_MATRIZ):
        coluna = input('LINHA '+  repr(i) + ", COLUNA:") # de 0 a 11, tem 12 colunas
        # tendo a linha i, descobrir em qual pilha(0, 1 ou 2) de placas está essa linha
        pilha = i/LINHAS;
        print('pilha: ' + repr(pilha))

        #descobrir a linha da placa, usado na matriz de bytes
        linha_da_placa = i%LINHAS;
        print("linha da placa: " + repr(linha_da_placa))

        #descobrir a coluna da placa, usado na matriz de bytes
        coluna_da_placa = int(coluna%COLUNAS);
        print("coluna da placa: "+repr(coluna_da_placa))

        #descobrir o nº da placa(de 0 a 8)
        n_placa = int(pilha*ORDEM + coluna/4);
        print("número placa :"+ repr(n_placa))

        mensagem[linha_da_placa][n_placa] |= 0x01 << (7-coluna_da_placa); 
        print(">> " + "{0:b}".format(mensagem[linha_da_placa][n_placa]))  
        print(">> ""{0:x}".format(mensagem[linha_da_placa][n_placa]))
        print(mensagem[linha_da_placa][n_placa])
    print(hex(mensagem)) 
    return mensagem

def MandarDados(mensagem):
    i=0
    j=0
    mensagem = MontarExemplo(mensagem)
    print("")
    print(mensagem)
    for i in xrange (0, LINHAS):
        for j in xrange (0, PLACAS):
            ser.write(chr(255))
            ser.write(chr(mensagem[i][j]))
            print(hex(mensagem[i][j]))
        ser.write('A')
        print(ser.read(1))
    return mensagem

def MontarExemplo(mensagem):
    # mensagem = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'),bytearray(b'\x02\x02\x02\x02\x02\x02\x02\x02\x02'),bytearray(b'\x04\x04\x04\x04\x04\x04\x04\x04\x04'),bytearray(b'\x06\x06\x06\x06\x06\x06\x06\x06\x06'),bytearray(b'\x08\x08\x08\x08\x08\x08\x08\x08\x08'),bytearray(b'\x0A\x0A\x0A\x0A\x0A\x0A\x0A\x0A\x0A'),bytearray(b'\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C\x0C'),bytearray(b'\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E\x0E') 
    mensagem = (bytearray(b'\x10\x00\x00\x00\x10\x00\x00\x00\x10'), bytearray(b'B\x02\x02\x02B\x02\x02\x02B'), bytearray(b'D\x04\x04\x04D\x04\x04\x04D'), bytearray(b'&\x06\x06\x06&\x06\x06\x06&'), bytearray(b'H\x08\x08\x08H\x08\x08\x08H'), bytearray(b'*\n\n\n*\n\n\n*'), bytearray(b'L\x0c\x0c\x0cL\x0c\x0c\x0c,'), bytearray(b'\x1e\x0e\x0e\x0e\x1e\x0e\x0e\x0e\x1e'))
    print(mensagem)
    return mensagem

def SAIR():
    ser.close()
    exit()
    return 

while 1:
    val = raw_input("0 - Montar Exemplo  1 - Limpar Matriz  2 - Configurar Matriz  3 - Mandar Dados  4 - SAIR: ")
    if ( val == '1' ): m = LimparMatriz()
    if ( val == '2' ): m = ConfigurarMatriz(m)
    if ( val == '3' ): m = MandarDados(m)
    if ( val == '4' ): SAIR()
    if ( val == '0' ): m = MontarExemplo(m)