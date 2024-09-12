import socket
import threading
import struct
import json
import os #acabei precisando pra puxar o nome dos diretorios dos jsons

from models.client import Cliente

############################################
diretorio_do_servidor = os.path.dirname(__file__)
diretorio_dos_BD      = os.path.join(diretorio_do_servidor, '..', '..', 'dados')

def carregar_rotas():
    diretorio_das_rotas = os.path.join(diretorio_do_servidor, 'rotas.json')
    with open(diretorio_das_rotas, 'r') as rotasBD:
        return json.load(rotasBD)

def carregar_passagens():
    diretorio_das_passagens = os.path.join(diretorio_do_servidor, 'passagens.json')
    with open(diretorio_das_passagens, 'r') as passagensBD:
        return json.load(passagensBD)

def atualizar_rotas(rotas):
    diretorio_das_rotas = os.path.join(diretorio_do_servidor, 'rotas.json')
    with open(diretorio_das_rotas, 'w') as rotasBD:
        json.dump(rotas, rotasBD, ident=4) # O ident aqui eh so pra ficar bonitinho

def atualizar_passagens(passagens):
    diretorio_das_passagens = os.path.join(diretorio_do_servidor, 'passagens.json')
    with open(diretorio_das_passagens, 'w') as passagensBD:
        json.dump(passagens, passagensBD, ident=4)

def comprar_passagem(cidade_saida, cidade_chegada):
    rotas = carregar_rotas()
    
    for rota in rotas:
        if (rota['cidadeSaida']==cidade_saida) and (rota['cidadeChegada']==cidade_chegada):
            if (rota['assentos_disponiveis']>0):
                rota['assentos_disponiveis'] -=1
                atualizar_rotas(rotas)
            
            # Como o BD das passagens ainda esta em branco eu deixei so esses 2 atributos mesmo
            nova_passagem = {
                "cidadeSaida": cidade_saida,
                "cidadeChegada": cidade_chegada
            }

            passagens = carregar_passagens()
            passagens.append(nova_passagem)
            atualizar_passagens(passagens)
            
            return f"Passagem criada: {nova_passagem}"
    return f"Nao tem nenhum trecho entre essas cidades com assentos disponiveis"

def tratar_cliente2(conexao, endereco):
    print(f"Conexão estabelecida com {endereco}")
    espacos()
    try:
        login_data = conexao.recv(1024).decode()
        identificador, senha = login_data.split(',')
        if Cliente.login(identificador, senha):
            conexao.sendall(b"Login bem-sucedido")
            print(f"Cliente [ID:{identificador}] {endereco} fez login com sucesso")
        else:
            conexao.sendall(b"Login falhou")
            conexao.close()
            return
    except Exception as e:
        print(f"Erro ao processar login: {e}")
        conexao.close()
    while True:
        mensagem = conexao.recv(1024).decode()
        print(f"Até aqui ta funcionando. a mensagem que chegou foi {mensagem}\n")

        operacao, cidade_saida, cidade_chegada = mensagem.split('|')

        # Sim, so tem a compra por enquanto...
        if (operacao == '1'):
            resposta = comprar_passagem(cidade_saida, cidade_chegada)
    
    conexao.sendall(resposta.encode())
    conexao.close()

############################################

def espacos():
    print("=-=-=-=-=-=-=-=-=-=-=-=-==-=-\n")
    
def ativo():
    return True

def tratar_cliente(conexao, endereco):
    print(f"Conexão estabelecida com {endereco}")
    espacos()
    
    # Recebe dados de login do cliente
    try:
        login_data = conexao.recv(1024).decode()
        identificador, senha = login_data.split(',')
        if Cliente.login(identificador, senha):
            conexao.sendall(b"Login bem-sucedido")
            print(f"Cliente [ID:{identificador}] {endereco} fez login com sucesso")
        else:
            conexao.sendall(b"Login falhou")
            conexao.close()
            return
    except Exception as e:
        print(f"Erro ao processar login: {e}")
        conexao.close()
        return

    while True:
        try:
            data = conexao.recv(1024)
            if not data:
                break
            numero_recebido = struct.unpack('!I', data)[0]
            print(f"Cliente {endereco} enviou: {numero_recebido}")
            conexao.sendall(struct.pack('!I', numero_recebido))
        except ConnectionResetError:
            break

    print(f"Conexão encerrada com {endereco}")
    conexao.close()

def main():
    IP_SERVIDOR = '127.0.0.1'
    PORTA_SERVIDOR = 5000

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP_SERVIDOR, PORTA_SERVIDOR))
    servidor.listen()
    ativo()

    print(f"Servidor escutando no IP {IP_SERVIDOR} e porta {PORTA_SERVIDOR}")

    while True:
        conexao, endereco = servidor.accept()
        print(f"Nova conexão de {endereco}")

        #cliente_thread = threading.Thread(target=tratar_cliente, args=(conexao, endereco))
        cliente_thread = threading.Thread(target=tratar_cliente2, args=(conexao, endereco))

        cliente_thread.start()
    

