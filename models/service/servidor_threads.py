import socket
import threading
import struct
import json
import os
from pathlib import Path
# from models.client import Cliente

#Criados os 2 MUTEX que irão controlar as operações de compra e cancelamento.
mutex = threading.Lock()

#Definição de diretórios para facilitar outras funções.
diretorio_do_servidor = Path(__file__).parent
diretorio_dos_BD = diretorio_do_servidor.parent.parent / 'dados'

#Função para carregar dados de forma genérica
def carregar_dados(arquivo):
    try:
        with open(arquivo, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {arquivo}")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    return None

#Função para salvar dados de forma genérica
def salvar_dados(arquivo, BD):
    try:
        with open(arquivo, 'w') as arquivo:
            json.dump(BD, arquivo, indent=4)
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")

#Funções específicas para carregar as rotas, passagens e usuarios. Elas rotornam seus respectivos Bancos de Dados(BD)
def carregar_rotas():
    diretorio_das_rotas = os.path.join(diretorio_dos_BD, 'rotas.json')
    return carregar_dados(diretorio_das_rotas)


def carregar_passagens():
    diretorio_das_passagens = os.path.join(diretorio_dos_BD, 'passagens.json')
    return carregar_dados(diretorio_das_passagens)


def carregar_usuarios():
    diretorio_dos_usuarios = os.path.join(diretorio_dos_BD, 'clientes.json')
    return carregar_dados(diretorio_dos_usuarios)

#Funções para atualizar os bancos de dados. Elas recebem um BD que foi editado(como 'rotas') e chama a função
#'salvar_dados' para realizar o dump no arquivo correto.
def atualizar_rotas(rotas):
    diretorio_das_rotas = os.path.join(diretorio_dos_BD, 'rotas.json')
    salvar_dados(diretorio_das_rotas, rotas)


def atualizar_passagens(passagens):
    diretorio_das_passagens = os.path.join(diretorio_dos_BD, 'passagens.json')
    salvar_dados(diretorio_das_passagens, passagens)

def atualizar_usuarios(usuarios):
    diretorio_dos_usuarios = os.path.join(diretorio_dos_BD, 'clientes.json')
    salvar_dados(diretorio_dos_usuarios, usuarios)

#Função para realizar o login, ela recebe o ID e a senha e compara a um usuário do BD 'clientes' e retorna uma mensagem
#que vai ser interpretada no cliente como uma autorização (ou não) para prosseguir com o menu
def logar(id, senha, usuarios):
    if usuarios is None:
        print("A lista de usuarios esta vazia")
    for user in usuarios:
        if user['id'] == id and user['senha'] == senha:
            return "Logado com sucesso"
    return "Login falhou"

#Função para contar o numero de passagens já criadas, importante para determinar o ID de uma nova passagem a ser gerada
def contar_passagens(passagens):
    contador = 1
    for passagem in passagens:
        contador +=1
    return contador

#Essa função executa a compra de uma passagem, detalhe que o processo de compra envolve mais do que só essa função, as etapas
#desse processo são determinadas no cliente.
def comprar_passagem(userID, rotas_a_serem_compradas , rotas, passagens, usuarios):
    # for rota in rotas:
    #     if rota['ID'] == rotaID:
    #         print("rota encontrada")
    #         if rota['assentos_disponiveis'] > 0:
    #             print("tem assentos disponiveis")
    #             cont = contar_passagens(passagens)
    #             print(f"\n\nAs informações para criar a passagem: {cont}, {userID}\n\n")
    #             nova_passagem = {
    #                 "id_passagem": cont,
    #                 "cliente_id": userID,
    #                 "rota": rota['trecho'],
    #                 "estaCancelado": False
    #             }
    #             print(f"foi criada: {nova_passagem}")
    #             passagens.append(nova_passagem)
    #
    #             for user in usuarios:
    #                 if user['id'] == userID:
    #                     array = user['passagens']
    #                     array.append(nova_passagem)
    #
    #             rota['assentos_disponiveis'] -= 1
    #             with mutex:
    #                 atualizar_rotas(rotas)
    #                 atualizar_passagens(passagens)
    #                 atualizar_usuarios(usuarios) 
    #
    #             return "Passagem criada com sucesso"
    #         else:
    #             return "Sem assentos disponíveis"
    # return "Rota não encontrada"

    rotas_sem_vagas = []
    passagens_para_registrar = []
    
    for rota_compra in rotas_a_serem_compradas:
        for rota_no_BD in rotas:
            if rota_compra == rota_no_BD['ID']:
                print(f"Rota com ID:{rota_compra} encontrada.")
                with mutex:
                    if rota_no_BD['assentos_disponiveis'] > 0:
                        print(f"Há assentos disponíveis na rota {rota_compra}.")
                        # Atualiza o contador a cada nova passagem
                        cont = contar_passagens(passagens)
                        contar_novamente = cont + len(passagens_para_registrar)  
                        print(f"As informações para a compra são: ID:{contar_novamente}, usuario:{userID}, rota:{rota_no_BD['trecho']}")
                        nova_passagem = {
                            "id_passagem": contar_novamente, 
                            "cliente_id": userID,
                            "rota": rota_no_BD['trecho'],
                            "estaCancelado": False
                        }
                        print(f"Foi criada a passagem {nova_passagem['id_passagem']}.")
                        passagens_para_registrar.append(nova_passagem)
                        rota_no_BD['assentos_disponiveis'] -= 1
                        atualizar_rotas(rotas)
                    else:
                        rotas_sem_vagas.append(rota_no_BD)

    if len(rotas_sem_vagas) == 0:
        with mutex:
            for p in passagens_para_registrar:
                passagens.append(p)
                for u in usuarios:
                    if p['cliente_id'] == u['id']:
                        historico = u['passagens']
                        historico.append(p)
            atualizar_passagens(passagens)
            atualizar_usuarios(usuarios) 
        return 'Compra realizada'

    elif len(rotas_sem_vagas) == len(rotas_a_serem_compradas):
        return 'Acabaram as vagas'
    else:
        with mutex:
            for p in passagens_para_registrar:
                for r in rotas:
                    if p['rota'] == r['trecho']:
                        r['assentos_disponiveis'] += 1
            atualizar_rotas(rotas)
        return rotas_sem_vagas                   


#Função que busca as passagens de um dado usuário e retorna todas que não estejam marcadas como canceladas.
def buscar_passagens_de_usuario(userID, usuarios):
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

#Função que cancela uma passagem, para todos os propósitos a requerida passagem não existe mais, contudo
#o registro dela permanece no BD das passagens e nas passagens do usuário no BD dos clientes, porém marcado
#como passagem cancelada.
def cancelar_passagem(passagemID, userID, passagens, usuarios):
    # with mutex_cancelamento:
    print("carregou o BD")
    for passagem in passagens:
        if passagem['id_passagem'] == int(passagemID):
            print("A passagem foi encontrada.")
            if passagem['estaCancelado'] != 1:
                passagem['estaCancelado'] = 1
                for user in usuarios:
                    if user['id'] == userID:
                        for p in user['passagens']:
                            if int(p['id_passagem']) == int(passagemID):
                                p['estaCancelado'] = 1
                with mutex:
                    atualizar_passagens(passagens)
                    atualizar_usuarios(usuarios)
                return "Passagem cancelada com sucesso."
            else:
                return "Essa passagem já foi cancelada"
    return "Passagem não encontrada."

#Função para mostrar as rotas disponíveis para compra a partir da solicitação do cliente
def mostrar_rotas(rotas):
    rotas_disponiveis = []
    for rota in rotas:
        if rota['assentos_disponiveis']>0:
            rotas_disponiveis.append(rota)
    print(f"tem um total de {len(rotas_disponiveis)} rotas disponiveis")
    for r in rotas_disponiveis:
        print(f"{r['trecho']}")
    return rotas_disponiveis

#Essa função interpreta a solicitação feita para o servidor, ela separa o 'opcode' da mensagem, seleciona
#a função a ser executada e envia os argumentos para sua execução.
def tratar_cliente(conexao_servidor, usuarios, passagens, rotas):
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
                resultado = logar(conteudo['id'], conteudo['senha'], usuarios)
            elif opcode == 2:
                resultado = mostrar_rotas(rotas)
            elif opcode == 3:
                resultado = comprar_passagem(conteudo['cliente_id'], conteudo['rotas_a_serem_compradas'], rotas, passagens, usuarios)
            elif opcode == 4:
                resultado = buscar_passagens_de_usuario(conteudo['cliente_id'], usuarios)
            elif opcode == 5:
                resultado = cancelar_passagem(conteudo['id_passagem'], conteudo['userID'], passagens, usuarios)
            else:
                resultado = "Operação inválida"

            conexao_servidor.sendall(json.dumps(resultado).encode())
    except Exception as e:
        print(f"Erro ao tratar cliente: {e}")
    finally:
        conexao_servidor.close()

# Essa função mantém o servidor ativo e conectado no endereço, ela também cria novas threads para conexões (até 8)
# e carrega os BD que serão usados nas funções.
def main():
    IP_SERVIDOR = '127.0.0.1'
    PORTA_SERVIDOR = 65432

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((IP_SERVIDOR, PORTA_SERVIDOR))
    servidor.listen(8)

    rotas = carregar_rotas()
    usuarios = carregar_usuarios()
    passagens = carregar_passagens()

    print("Servidor escutando...")

    while True:
        conexao_servidor, endereco_cliente = servidor.accept()
        print(f"Nova conexão de {endereco_cliente}")
        cliente_thread = threading.Thread(target=tratar_cliente, args=(conexao_servidor, usuarios, passagens, rotas))
        cliente_thread.start()


if __name__ == "__main__":
    main()
