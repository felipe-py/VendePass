import socket
import threading
import struct

from app.models.cliente.Cliente import Cliente


def espacos():
    print("=-=-=-=-=-=-=-=-=-=-=-=-==-=-\n")

def tratar_cliente(conexao, endereco):
    print(f"Conexão estabelecida com {endereco}")
    espacos()
    
    # Recebe dados de login do cliente
    try:
        login_data = conexao.recv(1024).decode()
        identificador, senha = login_data.split(',')
        if Cliente.login(identificador, senha):
            conexao.sendall(b"Login bem-sucedido")
            print(f"Cliente [ID:{identificador}] {endereco} fez login com sucesso")
        else:
            conexao.sendall(b"Login falhou")
            conexao.close()
            return
    except Exception as e:
        print(f"Erro ao processar login: {e}")
        conexao.close()
        return

    while True:
        try:
            data = conexao.recv(1024)
            if not data:
                break
            numero_recebido = struct.unpack('!I', data)[0]
            print(f"Cliente {endereco} enviou: {numero_recebido}")
            conexao.sendall(struct.pack('!I', numero_recebido))
        except ConnectionResetError:
            break

    print(f"Conexão encerrada com {endereco}")
    conexao.close()

def main():
    IP_SERVIDOR = '127.0.0.1'
    PORTA_SERVIDOR = 5000

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP_SERVIDOR, PORTA_SERVIDOR))
    servidor.listen()

    print(f"Servidor escutando no IP {IP_SERVIDOR} e porta {PORTA_SERVIDOR}")

    while True:
        conexao, endereco = servidor.accept()
        print(f"Nova conexão de {endereco}")

        cliente_thread = threading.Thread(target=tratar_cliente, args=(conexao, endereco))
        cliente_thread.start()

if __name__ == "__main__":
    main()
    
    