from Cliente import Cliente

def verificar_repeticao_id(cliente):
    clientes_cadastrados = cliente.carregar_clientes()
    for cadastros in clientes_cadastrados:
        if cadastros.id == cliente.id:
            return False
    return True

def cadastrar_cliente(cliente):
        if verificar_repeticao_id(cliente):
            cliente.salvar_cliente(cliente)
        else:
            print("Cliente previamente cadastrado")

