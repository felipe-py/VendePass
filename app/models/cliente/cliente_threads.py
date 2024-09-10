import socket
import struct

def login(cliente_socket):
    # Solicita credenciais do usuário
    identificador = input("Identificador: ")
    senha = input("Senha: ")
    
    # Envia as credenciais para o servidor
    login_data = f"{identificador},{senha}".encode()
    cliente_socket.sendall(login_data)
    
    # Recebe a resposta do servidor
    resposta = cliente_socket.recv(1024).decode()
    if resposta == "Login bem-sucedido":
        print("Login bem-sucedido!")
        return True
    else:
        print("Login falhou!")
        return False

def main():
    # Configurações do cliente
    IP_SERVIDOR = '127.0.0.1'  # IP do servidor
    PORTA_SERVIDOR = 5000       # Porta do servidor

    # Cria o socket TCP/IP do cliente
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((IP_SERVIDOR, PORTA_SERVIDOR))  # Conecta ao servidor

    try:
        # Realiza o login
        if not login(cliente):
            cliente.close()
            return

        while True:
            # Solicita um número inteiro ao usuário
            try:
                numero = int(input("Digite um número inteiro:\n"))  
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")
                continue

            # Envia o número ao servidor
            cliente.sendall(struct.pack('!I', numero))  # Empacota como inteiro de 4 bytes (big-endian)

            # Recebe e exibe a resposta do servidor
            data = cliente.recv(1024)
            if not data:
                print("Conexão perdida com o servidor.")
                break
            
            numero_recebido = struct.unpack('!I', data)[0]  # Desempacota o inteiro
            print(f"Recebido do servidor: {numero_recebido}")
            
            # Permite ao cliente sair se o número for 4
            if numero == 4:
                print("Encerrando a conexão...")
                break
    finally:
        cliente.close()  # Fecha a conexão

if __name__ == "__main__":
    main()
