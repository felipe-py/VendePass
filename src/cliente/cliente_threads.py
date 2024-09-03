import socket

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
            mensagem = input("Digite uma mensagem para enviar ao servidor: ")
            cliente.sendall(mensagem.encode('utf-8'))

            # Recebe e exibe a resposta do servidor
            resposta = cliente.recv(1024)
            print(f"Resposta do servidor: {resposta.decode('utf-8')}")

            # Permite ao cliente sair
            if mensagem.lower() == 'sair':
                print("Encerrando a conexão...")
                break
    finally:
        cliente.close()  # Fecha a conexão

if __name__ == "__main__":
    main()
