from models.viagem.GerenciadorViagem import GerenciadorViagens

'''usuarios_cadastrados = Cliente.carregar_clientes()
if Cliente.login(2,44,usuarios_cadastrados):
    print("s")
else:
    print("n")'''

geren = GerenciadorViagens()
geren.diminuir_assentos("1")

print(geren.trechos['1'])

geren.aumentar_assentos("1")
print(geren.trechos["1"])

geren.adicionar_trecho(5,"Teresina -> Palmas")
geren.adicionar_trecho(6,"Palmas -> Goiânia")
geren.adicionar_trecho(7,"Goiânia -> Campo Grande")
geren.adicionar_trecho(8,"Campo Grande -> São Paulo")
geren.adicionar_trecho(9,"São Paulo -> Rio de Janeiro")

geren.diminuir_assentos("2")
print(geren.trechos["2"])
geren.diminuir_assentos("2")
print(geren.trechos["2"])
geren.realizar_viagem("2")
print(geren.trechos["2"])
