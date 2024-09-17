import socket
import json

HOST = '127.0.0.1'
PORT = 65432

def conectar():
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect(HOST, PORT)

    return s1

def desconectar(s1):
    s1.close()

def enviar_dados(s1, opcode, dados):
    mensagem = {
        "opcode":opcode,
        "dados": dados
    }

    s1.sendall(json.dumps(mensagem).encode())
    resposta = s1.recv(1024).decode()

    if (opcode == 2):
        return resposta
    if (opcode != 2):
        print(resposta)

def logout(s1):
    print("Adeus")
    login(s1)
    
    return


def login(s1):
    print("Para sair digite SAIR")
    id = input("Digite seu ID: ")
    if (id == 'SAIR'):
        desconectar(s1)
    senha = input("Digite sua senha: ")

    credenciais = {'id': id, 'senha': senha}

    resposta = enviar_dados(s1, 1, credenciais)
    if (resposta == "Logado com sucesso."):
        return id
    else:
        return Null

def mostrar_rotas(s1):
    mensagem = {} # Apenas para preservar o formato da mensagem ao servidor
    resposta = enviar_dados(s1, 2, mensagem)

    for rota in resposta:
        rotaID = rota['ID']
        trecho = rota['trecho']
        print(f"ID:{rotaID} Trecho:{trecho}\n")

    return


def comprar_passagem(s1, user):
    mostrar_rotas()
    rotaID = input("\nInsira o ID da rota desejada: ")

    mensagem = {
        'cliente_id': user,
        'rotaID': rotaID
    }

    try:
        reposta = enviar_dados(s1, 3, mensagem)
        rota = resposta['rota']

        print(f"{user} comprou uma passagem para a rota {rota}")

        return True
    finally:
        print("Alguma coisa deu errado, verifique o ID da rota inserido.\n")
        return False


def mostrar_passagens(s1, user):
    mensagem = {} # Apenas para manter a estrutura de envio de mensagens
    passagens = enviar_dados(s1, 4, mensagem)
    
    try:
        for passagem in passagens:
            id = passagem['id_passagem']
            rota = passagem['rota']

            print(f"ID:{id}  rota:{rota}")
            return True
    finally:
        return False

def cancelar_compra(s1, user):
    mostrar_passagens()
    passagemID = input("\nIsira o ID da passagem: ")

    mensagem = {
        'cliente_id': user,
        'id_passagem': passagemID
    }
    try:
        resposta = enviar_dados(s1, 5, mensagem)
        passagem = resposta['id_passagem']

        print(f"{user} cancelou a passagem {passagem}")

        return True
    finally:
        print("Alguma coisa deu errado, verifique o ID da passagem inserido.\n")
        return False

def menu(s1, user):
    print("1.Comprar uma passagem.\n")
    print("2.Cancelar uma compra.\n")
    print("3.Sair\n\n")

    operacao = input(": ")
    while (operacao != 3):
        while (operacao not in range(1,4)):
            operacao = input("Por favor, selecione uma opção válida\n: ")
        if (operacao == 1):
            comprar_passagem(s1, user)
        if (operacao == 2):
            cancelar_compra(s1, user)
    logout(s1)

def main():
    s1 = conectar()
    user = login(s1)

    menu(s1, user)
if __name__ == "__main__":
    main()
