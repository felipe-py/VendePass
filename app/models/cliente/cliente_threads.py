import socket
import struct

def main():
    # Configurações do cliente
    IP_SERVIDOR = '127.0.0.1'  # IP do servidor
    PORTA_SERVIDOR = 5000       # Porta do servidor

    # Cria o socket TCP/IP do cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((IP_SERVIDOR, PORTA_SERVIDOR))  # Conecta ao servidor

    try:
        while True:
            # Envia uma mensagem ao servidor
            numero = int(input("Digite um número inteiro:\n"))  
            cliente.sendall(struct.pack('!I', numero))  # Empacota como inteiro de 4 bytes (big-endian)

            # Recebe e exibe a resposta do servidor
            data = cliente.recv(1024)
            numero_recebido = struct.unpack('!I', data)[0]  # Desempacota o inteiro
            print(f"Recebido do servidor: {numero_recebido}")
            
            # Permite ao cliente sair
            if numero == 4:
                print("Encerrando a conexão...")
                break
    finally:
        cliente.close()  # Fecha a conexão

if __name__ == "__main__":
    main()
