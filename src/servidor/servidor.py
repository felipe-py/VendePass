import socket
import struct

def servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('127.0.0.1', 65432))  # IP local e porta

    server_socket.listen()
    print("Servidor escutando...")

    conn, addr = server_socket.accept()
    print(f"Conectado com {addr}")

    # Recebendo dados
    data = conn.recv(1024)
    numero_recebido = struct.unpack('!I', data)[0]  # Desempacota o inteiro

    # Respondendo ao cliente com o mesmo número
    conn.sendall(struct.pack('!I', numero_recebido))   # Reenvia o número empacotado

    conn.close()

servidor()
