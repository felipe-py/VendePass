import socket
import threading
import json
import Rotas
import Passagem
import DateTime

import socket
import threading
import json
from Rotas import Rota
from Passagem import Passagem
from datetime import datetime


def buscarObjeto(objeto, bancoDeDados):
    if objeto in bancoDeDados:
        return bancoDeDados[objeto]
    return None

def carregarBancoDeDados(bancoDeDados):
    with open(bancoDeDados, 'r') as banco:
        return json.load(banco)

def comprarPassagem(usuario, rota, bancoDeUsuarios, bancoDeRotas, bancoDePassagens):
    if not buscarObjeto(usuario, bancoDeUsuarios):
        return None
    if not buscarObjeto(rota, bancoDeRotas):
        return None
    if bancoDeRotas[rota]['numeroAssentos'] < 1:
        return None

    bancoDeRotas[rota]['numeroAssentos'] -= 1
    novaPassagem = Passagem(datetime.now(), reserva=False, cidadeSaida=bancoDeRotas[rota]['cidadeSaida'],
                            cidadeChegada=bancoDeRotas[rota]['cidadeChegada'], poltrona=0, estaPago=True, estaCancelado=False)
    
    bancoDePassagens[usuario] = novaPassagem.__dict__  # Adicionar ao banco de passagens
    
    with open('passagens.json', 'w') as passagens:
        json.dump(bancoDePassagens, passagens)
    return novaPassagem

def reservarPassagem(usuario, rota, bancoDeUsuarios, bancoDeRotas, bancoDePassagens):
    if not buscarObjeto(usuario, bancoDeUsuarios):
        return None
    if not buscarObjeto(rota, bancoDeRotas):
        return None
    if bancoDeRotas[rota]['numeroAssentos'] < 1:
        return None

    bancoDeRotas[rota]['numeroAssentos'] -= 1
    novaPassagem = Passagem(datetime.now(), reserva=True, cidadeSaida=bancoDeRotas[rota]['cidadeSaida'],
                            cidadeChegada=bancoDeRotas[rota]['cidadeChegada'], poltrona=0, estaPago=False, estaCancelado=False)
    
    bancoDePassagens[usuario] = novaPassagem.__dict__  # Adicionar ao banco de passagens
    
    with open('passagens.json', 'w') as passagens:
        json.dump(bancoDePassagens, passagens)
    return novaPassagem

def pagarReserva(passagem, bancoDePassagens):
    if not buscarObjeto(passagem, bancoDePassagens):
        return False
    if bancoDePassagens[passagem]['estaPago']:
        return False
    bancoDePassagens[passagem]['estaPago'] = True
    
    with open('passagens.json', 'w') as passagens:
        json.dump(bancoDePassagens, passagens)
    
    return True

def cancelarCompra(passagem, rota, bancoDePassagens, bancoDeRotas):
    if not buscarObjeto(passagem, bancoDePassagens):
        return False
    if bancoDePassagens[passagem]['estaCancelado']:
        return False
    
    bancoDePassagens[passagem]['estaCancelado'] = True
    bancoDeRotas[rota]['numeroAssentos'] += 1
    
    with open('passagens.json', 'w') as passagens:
        json.dump(bancoDePassagens, passagens)
    
    with open('rotas.json', 'w') as rotas:
        json.dump(bancoDeRotas, rotas)
    
    return True

def carregarUsuarios():
    with open('usuarios.json', 'r') as f:
        return json.load(f)

def verificarLogin(usuario, bancoDeUsuarios):
    login = usuario.get('login')
    senha = usuario.get('senha')

    if login in bancoDeUsuarios and bancoDeUsuarios[login] == senha:
        print('Logado com Sucesso')
        return True
    else:
        print('Login falhou')
    return False

def novoCliente(conn, addr, bancoDeUsuarios, bancoDeRotas, bancoDePassagens):
    print(f'Nova conexão com {addr}')
    
    try:
        while True:
            credenciaisRecebidas = conn.recv(1024).decode('utf-8')
            
            if not credenciaisRecebidas:
                break
            else:
                credenciais = json.loads(credenciaisRecebidas)
                estaLogado = verificarLogin(credenciais, bancoDeUsuarios)
            
            if estaLogado:
                conn.sendall("Logado com sucesso".encode('utf-8'))
                # Aqui você chama as funções para comprar, reservar, etc.
            else:
                conn.sendall("Falha no login".encode('utf-8'))
    finally:
        conn.close()

HOST = ''        # só declarando o host que vai ser usado na tupla "origem" 
PORT = 8000      # Porta que vai ser usada na conexao

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # criando um novo socket usando endereco IPv4 (AF_INET) do tipo stream de dados, ou TCP (SOCK_STREAM), preferi nao arriscar o "fileno"

origem = (HOST, PORT)  # essa tupla "guarda" a informacao do servidor em que se desej conectar e a porta escolhida, usado nas funcoes do socket 
tcp.bind(origem)       # Ligando o socket a origem
tcp.listen(10)         # Escutando até 10 conexões em fila

bancoDeUsuarios = carregarUsuarios()

# Aqui eh a execucao do programa propriamente dita
while True:
    con, cliente = tcp.accept()                     # Aceita uma nova conexão com "cliente"
    print(f"Nova conexão aceita de {cliente}")      # Mensagem para feedback

    thread = threading.Thread(target=novoCliente, args=(con, cliente, bancoDeUsuarios))          # Criando uma nova thread para a conexao com "cliente"
    thread.start()                                                              # Iniciando a thread
    
    print(f'Número de conexões ativas: {threading.active_count() - 1}')         # Mostra o número de threads ativas

print("FIM")  # Esse print nao acontece na pratica, pois nao tem um break no while, mas caso no futuro apliquemos algo depois do fim da execucao.

