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
    
    
    return mensagem
def LimparMatrizNaPlaca():
    ser.write(b'\x42') # apagar a matriz física
    return

def ConfigurarMatriz(mensagem):
    componentes = MostrarComponentes()
    # o vetor coluna[] recebe 24 valores para as 24 linhas da matriz desse sistema
    print('DIGITE A CONFIGURAÇÃO DA MATRIZ (24 linhas por 12 colunas)')
    for i in range (LINHAS_MATRIZ):
        coluna_aux = input(componentes[i]+" COLUNA: ") # de 0 a 11, tem 12 colunas
        if(coluna_aux==''):
            coluna = 99
        else:
            coluna = int(coluna_aux)

        if((coluna>-1) and (coluna<12)):
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

            
            coluna_de_placas = coluna/4
            # descobrir o nº da placa(de 0 a 8)
            n_placa = int(pilha*ORDEM + coluna_de_placas)
            if(pilha==1):
                n_placa = (n_placa-8)*-1
            print("número placa :", n_placa)

            mb = int.from_bytes(mensagem[linha_da_placa][n_placa],byteorder='big',signed=False)
            mb |= (1 << (7-coluna_da_placa))
            mensagem[linha_da_placa][n_placa] = mb.to_bytes(1, byteorder='big',signed=False)
            print(">> " + "{0:b}".format(mb))  
            print(">> ""{0:x}".format(mb))   
    print(mensagem)
    return mensagem

def MandarDados(mensagem):
    tempo = 0.01
    for i in range (LINHAS):
        for j in range (PLACAS-1,-1,-1):
            print("linha ",i, "placa ", j)
            time.sleep(tempo)
            ser.write(b'\xff')
            ser.write(mensagem[i][j])
            print(mensagem[i][j])
            time.sleep(tempo)
        ser.write(b'\x41')
        time.sleep(tempo)
    return mensagem

def MudarTensao():
    dac_value = float(input("Digite o valor da tensão variável(0-5V): "))
    dac_value_to_send = bytearray(struct.pack("f", dac_value)) 
    dac_value_to_send.insert(0,67)
    ser.write(dac_value_to_send)
    return

def LerEntradaAnalogica():
    ser.write(b'\x44')
    ser_bytes = ser.read(4)
    float_value = struct.unpack("f", ser_bytes)
    print (float_value)
    # value = ser.readline()
    # print(value)
    time.sleep(0.5)
    return 

def MostrarComponentes():
    componentes = [
    "linha 0 - gnd",
    "linha 1 - vcc",
    "linha 2 - tensão variável 0-5V",
    "linha 3 - entrada analógica",
    "linha 4 - 10k(pin1)",
    "linha 5 - 10k(pin2)",
    "linha 6 - 100k(pin1)",
    "linha 7 - 100k(pin2)",
    "linha 8 - lm324-ampop(gnd)",
    "linha 9 - lm324-ampop(2out)",
    "linha 10 - lm324-ampop(2in-)",
    "linha 11 - lm324-ampop(2in+)",
    "linha 12 - lm324-ampop(Vcc)",
    "linha 13 - lm324-ampop(1in+)",
    "linha 14 - lm324-ampop(1in-)",
    "linha 15 - lm324-ampop(1out)",
    "linha 16 - 220(pin1)",
    "linha 17 - 220(pin2)",
    "linha 18 - 1k(pin1)",
    "linha 19 - 1k(pin2)",
    "linha 20 -não conectada",
    "linha 21 -não conectada", 
    "linha 22 -não conectada", 
    "linha 23 -não conectada" 
    ]
    return componentes

def SAIR():
    ser.close()
    exit()
    return 

while 1:
    val = input("0 - Limpa Matriz Física\n1 - Limpar Variável da Matriz\n2 - Configurar Matriz\n3 - Mandar Dados\n4 - Mudar Tensão\n5 - Mostrar Componentes\n6 - Ler Entrada Analógica \n7 - SAIR\nEscolha: ")
    if ( val == '0' ): LimparMatrizNaPlaca()
    if ( val == '1' ): m = LimparMatriz()
    if ( val == '2' ): m = ConfigurarMatriz(m)
    if ( val == '3' ): m = MandarDados(m)
    if ( val == '4' ): MudarTensao()
    if ( val == '5' ):
        componentes = MostrarComponentes()
        for i in range (LINHAS_MATRIZ):
            print(componentes[i])
    if ( val == '6' ): LerEntradaAnalogica() 
    if ( val == '7' ): SAIR()