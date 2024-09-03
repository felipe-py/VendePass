from cliente.Cliente_main import Usuario

def verificar_repeticao_id(usuario):
    usuarios_cadastrados = Usuario.carregar_usuarios()
    for cadastros in usuarios_cadastrados:
        if cadastros.id == usuario.id:
            return False
    return True

def cadastrar_usuario(usuario):
        if verificar_repeticao_id(usuario):
            Usuario.salvar_usuario(usuario)
        else:
            print("Usuario previamente cadastrado")