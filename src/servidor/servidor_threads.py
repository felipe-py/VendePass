import socket
import threading

# Função que trata cada cliente em uma thread separada
def tratar_cliente(conexao, endereco):
    print(f"Conexão estabelecida com {endereco}")
    while True:
        try:
            # Recebe dados do cliente
            dados = conexao.recv(1024)
            if not dados:
                break  # Se não há dados, encerra a conexão
            # Decodifica e exibe a mensagem recebida
            mensagem = dados.decode('utf-8')
            print(f"Cliente {endereco} enviou: {mensagem}")

            # Resposta para o cliente
            conexao.sendall(f"Mensagem recebida: {mensagem}".encode('utf-8'))
        except ConnectionResetError:
            break  # Se o cliente fechar a conexão abruptamente, encerra a thread

    print(f"Conexão encerrada com {endereco}")
    conexao.close()

def main():
    # Configurações do servidor
    IP_SERVIDOR = '127.0.0.1'  # IP local para testes
    PORTA_SERVIDOR = 5000       # Porta do servidor

    # Cria o socket TCP/IP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP_SERVIDOR, PORTA_SERVIDOR))  # Vincula IP e porta
    servidor.listen()  # Escuta conexões

    print(f"Servidor escutando no IP {IP_SERVIDOR} e porta {PORTA_SERVIDOR}")

    while True:
        # Aceita conexões de clientes
        conexao, endereco = servidor.accept()
        print(f"Nova conexão de {endereco}")

        # Cria uma thread para tratar o cliente
        cliente_thread = threading.Thread(target=tratar_cliente, args=(conexao, endereco))
        cliente_thread.start()

if __name__ == "__main__":
    main()
