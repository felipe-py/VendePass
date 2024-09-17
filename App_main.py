import socket
import json

HOST = '127.0.0.1'
PORT = 65432

def conectar():
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((HOST, PORT))
    return s1

def desconectar(s1):
    s1.close()

def enviar_dados(s1, opcode, dados):
    mensagem = {
        "opcode": opcode,
        "dados": dados
    }
    s1.sendall(json.dumps(mensagem).encode())
    resposta = s1.recv(1024).decode()
    return json.loads(resposta)

def logout(s1):
    print("Adeus")
    desconectar(s1)

def login(s1):
    print("Digite SAIR para sair.")
    id = input("Digite seu ID: ")
    if id == "SAIR":
        desconectar(s1)
    senha = input("Digite sua senha: ")
    credenciais ={
        'id':id,
        'senha':senha
    } 
    resposta = enviar_dados(s1, 1, credenciais)

    if resposta == "Logado com sucesso":
        return id
    else:
        print("Falha na autenticação.")
        return None

def mostrar_rotas(s1):
    resposta = enviar_dados(s1, 2, {})
    print(f"{resposta}")
    for rota in resposta:
        print(f"ID: {rota['ID']} | Trecho: {rota['trecho']}")

def comprar_passagem(s1, user):
    mostrar_rotas(s1)
    rotaID = input("\nInsira o ID da rota desejada: ")

    mensagem = {
        'cliente_id': user,
        'rotaID': rotaID
    }

    resposta = enviar_dados(s1, 3, mensagem)
    print(resposta)

def mostrar_passagens(s1, user):
    mensagem = {'cliente_id': user}
    passagens = enviar_dados(s1, 4, mensagem)

    for passagem in passagens:
        print(f"ID: {passagem['id_passagem']} | Rota: {passagem['rota']}")

def cancelar_compra(s1, user):
    mostrar_passagens(s1, user)
    passagemID = input("\nInsira o ID da passagem: ")

    mensagem = {'id_passagem': passagemID, 'userID': user}
    resposta = enviar_dados(s1, 5, mensagem)
    print(resposta)

def menu(s1, user):
    while True:
        print("1. Comprar uma passagem")
        print("2. Cancelar uma compra")
        print("3. Sair")

        operacao = input(": ")

        if operacao == '1':
            comprar_passagem(s1, user)
        elif operacao == '2':
            cancelar_compra(s1, user)
        elif operacao == '3':
            logout(s1)
            break
        else:
            print("Por favor, selecione uma opção válida.")

def main():
    s1 = conectar()
    user = login(s1)

    if user:
        menu(s1, user)

if __name__ == "__main__":
    main()


<<<<<<< Updated upstream
mainCliente()
=======
>>>>>>> Stashed changes
