# import socket
# from models.client.Cliente import Cliente
#
# def verificar_repeticao_id(cliente):
#     clientes_cadastrados = cliente.carregar_clientes()
#     for cadastros in clientes_cadastrados:
#         if cadastros.id == cliente.id:
#             return False
#     return True
#
# def cadastrar_cliente(cliente):
#         if verificar_repeticao_id(cliente):
#             cliente.salvar_cliente(cliente)
#         else:
#             print("Cliente previamente cadastrado")
# #############################################################
#
# def solicitarResposta(solicitacao):
#
#     IP_SERVIDOR = '127.0.0.1'
#     PORTA_SERVIDOR = 5000
#
#     try: 
#         cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         cliente_socket.connect((IP_SERVIDOR, PORTA_SERVIDOR))
#
#         cliente_socket.sendall(solicitacao.encode())
#         resposta = cliente_socket.recv(1024).decode()
#         print(f"A resposta do servidor foi {resposta}")
#
#     finally:
#         cliente_socket.close()
#     return resposta
#
# def comprar_passagem():
#
#     cidadeSaida   = input("Qual eh a cidade de saida?\n")
#     cidadeChegada = input("Qual eh a cidade de chegada?\n")
#
#     operacao = "1"
#
#     solicitacao = f"{operacao}|{cidadeSaida}|{cidadeChegada}"
#     print(f"{solicitacao}")
#     resposta    = solicitarResposta(solicitacao)
#
#     print(f"{resposta}")
#
# def reservar_passagem():
#     print("Reservando Passagem")
#
# def pagar_reserva():
#     print("Pagando a reserva")
#
# def cancelar_compra():
#     print("Cancelando a compra")
#
#
