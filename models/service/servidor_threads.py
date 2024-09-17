import socket
import threading
import struct
import json
import os
from pathlib import Path
from models.client import Cliente

#Criados os 2 MUTEX que irão controlar as operações de compra e cancelamento.
mutex_compra = threading.Lock()
mutex_cancelamento = threading.Lock()

#definição de diretórios para facilitar outras funções.
diretorio_do_servidor = Path(__file__).parent
diretorio_dos_BD = diretorio_do_servidor.parent.parent / 'dados'


def carregar_dados(arquivo):
    try:
        with open(arquivo, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {arquivo}")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    return None


def salvar_dados(arquivo, BD):
    try:
        with open(arquivo, 'w') as arquivo:
            json.dump(BD, arquivo, indent=4)
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")


def carregar_rotas():
    diretorio_das_rotas = os.path.join(diretorio_dos_BD, 'rotas2.json')
    return carregar_dados(diretorio_das_rotas)


def carregar_passagens():
    diretorio_das_passagens = os.path.join(diretorio_dos_BD, 'passagens.json')
    return carregar_dados(diretorio_das_passagens)


def carregar_usuarios():
    diretorio_dos_usuarios = os.path.join(diretorio_dos_BD, 'clientes.json')
    return carregar_dados(diretorio_dos_usuarios)


def atualizar_rotas(rotas):
    diretorio_das_rotas = os.path.join(diretorio_dos_BD, 'rotas2.json')
    salvar_dados(diretorio_das_rotas, rotas)


def atualizar_passagens(passagens):
    diretorio_das_passagens = os.path.join(diretorio_dos_BD, 'passagens.json')
    salvar_dados(diretorio_das_passagens, passagens)

def atualizar_usuarios(usuarios):
    diretorio_dos_usuarios = os.path.join(diretorio_dos_BD, 'clientes.json')
    salvar_dados(diretorio_dos_usuarios, usuarios)

def logar(id, senha):
    usuarios = carregar_usuarios()
    if usuarios is None:
        print("A lista de usuarios esta vazia")
    for user in usuarios:
        if user['id'] == id and user['senha'] == senha:
            return "Logado com sucesso"
    return "Login falhou"


def contar_passagens():
    contador = 1
    passagens = carregar_passagens()
    for passagem in passagens:
        contador +=1
    return contador

def comprar_passagem(userID, rotaID):
    with mutex_compra:
        rotas = carregar_rotas()
        for rota in rotas:
            if rota['ID'] == rotaID:
                print("rota encontrada")
                if rota['assentos_disponiveis'] > 0:
                    print("conferiu o numero de assentos corretamente")
                    cont = contar_passagens()
                    print(f" As informações para criar a passagem: {cont}, {userID} ")
                    nova_passagem = {
                        "id_passagem": cont,
                        "cliente_id": userID,
                        "rota": rota['trecho'],
                        "estaCancelado": False
                    }
                    print(f"foi criada: {nova_passagem}")
                    passagens = carregar_passagens()
                    passagens.append(nova_passagem)
                    atualizar_passagens(passagens)

                    usuarios = carregar_usuarios()
                    for user in usuarios:
                        if user['id'] == userID:
                            array = user['passagens']
                            array.append(nova_passagem)
                    atualizar_usuarios(usuarios) 

                    rota['assentos_disponiveis'] -= 1
                    atualizar_rotas(rotas)

                    return "Passagem criada com sucesso"
                else:
                    return "Sem assentos disponíveis"
        return "Rota não encontrada"


def buscar_passagens_de_usuario(userID):
    usuarios = carregar_usuarios()
    passagens_validas = []
    for user in usuarios:
        if (user['id'] == userID):
            print("usuario encontrado")
            for passagem in user['passagens']:
                if passagem['estaCancelado'] == 0:
                    passagens_validas.append(passagem)
            print(f"{passagens_validas}")
            return passagens_validas
    return None


def cancelar_passagem(passagemID, userID):
    with mutex_cancelamento:
        passagens = carregar_passagens()
        print("carregou o BD")
        for passagem in passagens:
            if passagem['id_passagem'] == int(passagemID):
                print("A passagem foi encontrada.")
                if passagem['estaCancelado'] != 1:
                    passagem['estaCancelado'] = 1
                    atualizar_passagens(passagens)

                    usuarios = carregar_usuarios()
                    for user in usuarios:
                        if user['id'] == userID:
                            for p in user['passagens']:
                                if int(p['id_passagem']) == int(passagemID):
                                    p['estaCancelado'] = 1
                    atualizar_usuarios(usuarios)
                    return "Passagem cancelada com sucesso."
                else:
                    return "Essa passagem já foi cancelada"
        return "Passagem não encontrada."

def mostrar_rotas():
    rotas = carregar_rotas()
    rotas_disponiveis = []
    for rota in rotas:
        if rota['assentos_disponiveis']>0:
            rotas_disponiveis.append(rota)
    print(f"tem um total de {len(rotas_disponiveis)} rotas disponiveis")
    for r in rotas_disponiveis:
        print(f"{r['trecho']}")
    return rotas_disponiveis


def tratar_cliente(conexao_servidor):
    try:
        while True:
            mensagem = conexao_servidor.recv(1024).decode()
            if not mensagem:
                break
            print(f"Mensagem recebida: {mensagem}")
            dados = json.loads(mensagem)
            opcode = dados['opcode']
            conteudo = dados['dados']

            print(f"os dados enviados foram {conteudo}")
            if opcode == 1: 
                resultado = logar(conteudo['id'], conteudo['senha'])
            elif opcode == 2:  # Mostrar rotas
                resultado = mostrar_rotas()
            elif opcode == 3:  # Comprar passagem
                resultado = comprar_passagem(conteudo['cliente_id'], conteudo['rotaID'])
            elif opcode == 4:  # Buscar passagens
                resultado = buscar_passagens_de_usuario(conteudo['cliente_id'])
            elif opcode == 5:  # Cancelar passagem
                resultado = cancelar_passagem(conteudo['id_passagem'], conteudo['userID'])
            else:
                resultado = "Operação inválida"

            conexao_servidor.sendall(json.dumps(resultado).encode())
    except Exception as e:
        print(f"Erro ao tratar cliente: {e}")
    finally:
        conexao_servidor.close()


def main():
    IP_SERVIDOR = '127.0.0.1'
    PORTA_SERVIDOR = 65432

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((IP_SERVIDOR, PORTA_SERVIDOR))
    servidor.listen()

    print("Servidor escutando...")

    while True:
        conexao_servidor, endereco_cliente = servidor.accept()
        print(f"Nova conexão de {endereco_cliente}")
        cliente_thread = threading.Thread(target=tratar_cliente, args=(conexao_servidor,))
        cliente_thread.start()


if __name__ == "__main__":
    main()

