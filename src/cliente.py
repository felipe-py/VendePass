import socket
import struct

# Criação do socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexão ao servidor
client_socket.connect(('127.0.0.1', 65432))

# Enviando informação dada pelo usuário ao servidor

numero = int(input("Digite um número inteiro:\n"))
client_socket.sendall(str(numero).encode('utf-8'))
#client_socket.sendall(struct.pack('!I', numero))   MAIS EFICIENTE

# Recebendo resposta do servidor
data = client_socket.recv(1024)
print(f"Recebido do servidor: {data.decode()}")

client_socket.close()
