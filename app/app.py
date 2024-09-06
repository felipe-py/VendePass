from models.cliente.Cliente import Cliente

usuarios_cadastrados = Cliente.carregar_clientes()
if Cliente.login(2,44,usuarios_cadastrados):
    print("s")
else:
    print("n")