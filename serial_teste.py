# This Python file uses the following encoding: utf-8

import serial
import time
import struct

ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=2) 
try:
    ser.isOpen()
    time.sleep(2)
    print("Conexão serial aberta")
except:
    print("Erro")
    exit() 

LINHAS = 8 
COLUNAS = 4
LINHAS_MATRIZ = 24
COLUNAS_MATRIZ = 12 
PLACAS = 9
ORDEM = 3 

def LimparMatriz():
    mensagem = [[0 for i in range(PLACAS)] for j in range(LINHAS)]
    mensagem = [[b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00',b'\x00'],
    [b'\x02',b'\x02',b'\x02',b'\x02',b'\x02',b'\x02',b'\x02',b'\x02',b'\x02'],
    [b'\x04',b'\x04',b'\x04',b'\x04',b'\x04',b'\x04',b'\x04',b'\x04',b'\x04'],
    [b'\x06',b'\x06',b'\x06',b'\x06',b'\x06',b'\x06',b'\x06',b'\x06',b'\x06'],
    [b'\x08',b'\x08',b'\x08',b'\x08',b'\x08',b'\x08',b'\x08',b'\x08',b'\x08'],
    [b'\x0a',b'\x0a',b'\x0a',b'\x0a',b'\x0a',b'\x0a',b'\x0a',b'\x0a',b'\x0a'],
    [b'\x0c',b'\x0c',b'\x0c',b'\x0c',b'\x0c',b'\x0c',b'\x0c',b'\x0c',b'\x0c'],
    [b'\x0e',b'\x0e',b'\x0e',b'\x0e',b'\x0e',b'\x0e',b'\x0e',b'\x0e',b'\x0e'] ]
    
    ser.write(b'\x42') # apagar a matriz física
    return mensagem

def ConfigurarMatriz(mensagem):
    # o vetor coluna[] recebe 24 valores para as 24 linhas da matriz desse sistema
    print('DIGITE A CONFIGURAÇÃO DA MATRIZ (24 linhas por 12 colunas)')
    for i in range (LINHAS_MATRIZ):
        coluna = int(input('LINHA '+repr(i)+ ", COLUNA:")) # de 0 a 11, tem 12 colunas
        if((coluna>-1)and(coluna<11)):
            # coluna = int(input('LINHA '+repr(i)+ ", COLUNA:"))
            # tendo a linha i, descobrir em qual pilha(0, 1 ou 2) de placas está essa linha
            pilha = int(i/LINHAS)
            print('pilha: ' + repr(pilha))

            # descobrir a linha da placa, usado na matriz de bytes
            linha_da_placa = i % LINHAS
            print("linha da placa: " + repr(linha_da_placa))

            # descobrir a coluna da placa, usado na matriz de bytes
            coluna_da_placa = (int(coluna)%COLUNAS)
            print("coluna da placa: ", coluna_da_placa)

            # descobrir o nº da placa(de 0 a 8)
            n_placa = int(pilha*ORDEM + coluna/4)
            print("número placa :", n_placa)

            mb = int.from_bytes(mensagem[linha_da_placa][n_placa],byteorder='big',signed=False)
            mb |= (1 << (7-coluna_da_placa))
            mensagem[linha_da_placa][n_placa] = mb.to_bytes(1, byteorder='big',signed=False)
            
        print(">> " + "{0:b}".format(mb))  
        print(">> ""{0:x}".format(mb))
        print(mensagem[linha_da_placa][n_placa])
    print(mensagem)
    return mensagem

def MandarDados(mensagem):
    for i in range (LINHAS):
        for j in range (PLACAS-1,-1,-1):
            print("linha ",i, "placa ", j)
            time.sleep(0.5)
            ser.write(b'\xff')
            ser.write(mensagem[i][j])
            print(mensagem[i][j])
            time.sleep(0.5)
        ser.write(b'\x41')
        time.sleep(0.5)
    return mensagem

def MontarExemplo(mensagem):    
    mensagem = [[b' ', b'\x00', b'\x00', b'\x10', b'\x00', b'\x00', b'\x00', b'@', b'\x00'], [b'\x82', b'\x02', b'\x02', b'"', b'\x02', b'\x02', b'"', b'\x02', b'\x02'], [b'\x84', b'\x04', b'\x04', b'\x84', b'\x04', b'\x04', b'\x84', b'\x04', b'\x04'], [b'F', b'\x06', b'\x06', b'\x06', b'\x86', b'\x06', b'\x06', b'&', b'\x06'], [b'H', b'\x08', b'\x08', b'\x08', b'\x88', b'\x08', b'\x08', b'(', b'\x08'], [b'*', b'\n', b'\n', b'*', b'\n', b'\n', b'*', b'\n', b'\n'], [b'\x8c', b'\x0c', b'\x0c', b'\x8c', b'\x0c', b'\x0c', b'\x0c', b'\x0c', b'\x0c'], [b'\x1e', b'\x0e', b'\x0e', b'\x0e', b'N', b'\x0e', b'\x0e', b'\x0e', b'\x0e']]
    print(mensagem)
    return mensagem

def MudarTensao():
    dac_value = float(input("Digite o valor da tensão variável(0-5V): "))
    dac_value_to_send = bytearray(struct.pack("f", dac_value)) 
    dac_value_to_send.insert(0,67);
    ser.write(dac_value_to_send)
    
    return

def SAIR():
    ser.close()
    exit()
    return 

while 1:
    val = input("0 - Montar Exemplo\n1 - Limpar Matriz\n2 - Configurar Matriz\n3 - Mandar Dados\n4 - Mudar Tensão\n5 - SAIR\nEscolha a opção: ")
    if ( val == '0' ): m = MontarExemplo(m)
    if ( val == '2' ): m = ConfigurarMatriz(m)
    if ( val == '3' ): m = MandarDados(m)
    if ( val == '4' ): MudarTensao()
    if ( val == '5' ): SAIR()
    if ( val == '0' ): m = MontarExemplo(m)
