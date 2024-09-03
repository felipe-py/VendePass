from cliente.Cliente_main import Usuario

usuarios_cadastrados = Usuario.carregar_usuarios()
for usuario in usuarios_cadastrados:
    print(usuario)