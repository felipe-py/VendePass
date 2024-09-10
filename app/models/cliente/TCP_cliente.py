import socket
import json

def mostrarMenu():
    # Printar as opcoes
    # Pegar input do usuario
        # enquanto o input for invalido
        # pedir por um input valido
    # Se opcao selecionada for ...
        # invocar a funcao especifica

def juntarInformacoes():

def pedirPassagem():

def pedirRota():

def logar():  # Vai receber as credenciais e retornar um "mini dicionacio" com as informações
    login = input("digite seu login: ")
    senha = input("digite sua senha: ")

    return {'login':login, 'senha': senha}


HOST = '127.0.0.1' # Endereço padrao do servidor
PORT = 8000      # Porta inicial

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # OBS: usando o TCP/IP4


#user_input1 = input("Qual eh o endereço IP do servidor que voce quer se conectar?\n")
#if user_input1 != '': # Caso o usuario coloque algum valor de endereço IP
#    HOST = user_input1 # substitui o valor do servidor pelo servidor escolhido

#user_input2 = input("Em qual porta voce deseja se conectar?\n")
#if user_input2 != '':
#    PORT = int(user_input2) # substitui a porta em que se conectar

servidor = (HOST, PORT) # passando o servidor e a porta a se conectar como uma tupla
tcp.connect(servidor)   # realizando a conexao


status = ""
while status != "SAIR":
    
    #tcp.send(str.encode(mensagem)) # envia a mensagem
    #mensagem = input ("Qual eh a proxima mensagem?\nDigite SAIR para sair\n\n")
    
    credenciais = logar()
    
    tcp.sendall(json.dumps(credenciais).encode('utf-8'))

    confirmacao = tcp.recv(1024).decode('utf-8')
    print(confirmacao)

    procedimento = input("Qual a opcao selecionada?\n")
    tcp.sendall(procedimento.encode('utf-8'))


    
    status = input("Gostaria de SAIR?\n")
tcp.close() # finalizando a conexao
