import socket
import threading
import struct

def espacos():
    print("=-=-=-=-=-=-=-=-=-=-=-=-==-=-\n")

# Função que trata cada cliente em uma thread separada
def tratar_cliente(conexao, endereco):
    print(f"Conexão estabelecida com {endereco}")
    espacos()
    while True:
        try:
            # Recebe dados do cliente
            data = conexao.recv(1024)
            if not data:
                break  # Se não há dados, encerra a conexão
            # Decodifica e exibe a mensagem recebida
            numero_recebido = struct.unpack('!I', data)[0]  # Desempacota o inteiro
            print(f"Cliente {endereco} enviou: {numero_recebido}")
            # Respondendo ao cliente com o mesmo número
            conexao.sendall(struct.pack('!I', numero_recebido))   # Reenvia o número empacotado

        except ConnectionResetError:
            break  # Se o cliente fechar a conexão abruptamente, encerra a thread

    print(f"Conexão encerrada com {endereco}")
    espacos()
    conexao.close()

def main():
    # Configurações do servidor
    IP_SERVIDOR = '127.0.0.1'  # IP local para testes
    PORTA_SERVIDOR = 5000       # Porta do servidor

    # Cria o socket TCP/IP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP_SERVIDOR, PORTA_SERVIDOR))  # Vincula IP e porta
    servidor.listen()  # Escuta conexões

    espacos()
    print(f"Servidor escutando no IP {IP_SERVIDOR} e porta {PORTA_SERVIDOR}")
    espacos()

    while True:
        # Aceita conexões de clientes
        conexao, endereco = servidor.accept()
        espacos()
        print(f"Nova conexão de {endereco}")
        espacos()

        # Cria uma thread para tratar o cliente
        cliente_thread = threading.Thread(target=tratar_cliente, args=(conexao, endereco))
        cliente_thread.start()

if __name__ == "__main__":
    main()
