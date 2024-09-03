import socket
import struct

def cliente():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(('127.0.0.1', 65432))

    numero = int(input("Digite um número inteiro:\n"))  
    client_socket.sendall(struct.pack('!I', numero))  # Empacota como inteiro de 4 bytes (big-endian)

    data = client_socket.recv(1024)
    numero_recebido = struct.unpack('!I', data)[0]  # Desempacota o inteiro
    print(f"Recebido do servidor: {numero_recebido}")

    client_socket.close()

cliente()
