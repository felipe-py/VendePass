import socket
import struct

def servidor():

    # Criação do socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vinculando o socket ao endereço e porta
    server_socket.bind(('127.0.0.1', 65432))  # IP local e porta

    # Colocando o socket em modo de escuta, pronto para aceitar conexões
    server_socket.listen()

    print("Servidor escutando...")

    # Aceitando conexões de clientes
    conn, addr = server_socket.accept()
    print(f"Conectado com {addr}")

    # Recebendo dados
    data = conn.recv(1024)
    numero_recebido = int(data.decode('utf-8'))

    # Respondendo ao cliente

    conn.sendall(str(numero_recebido).encode('utf-8'))
    #conn.sendall(struct.pack('!I', numero_recebido))    MAIS EFICIENTE

    # Fechando a conexão
    conn.close()
