
'''usuarios_cadastrados = Cliente.carregar_clientes()
if Cliente.login(2,44,usuarios_cadastrados):
    print("s")
else:
    print("n")'''

'''geren = GerenciadorViagens()
for chave, valor in geren.trechos.items():
    print(f"Trecho {chave} => {valor.trecho}")
    print(f"Assentos disponíveis => {valor.ASSENTOS}\n")

print("Para escolher um trecho digite seu número correspondente:")'''

'''geren.diminuir_assentos("1")

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
print(geren.trechos["2"])'''

from models.viagem.GerenciadorViagem import GerenciadorViagens


def mostrarMenu():
    lista_opcoes = ["1","2","3","4"]
    lista_opcoes_trecho = ['1','2','3','4','5','6','7','8','9']
    geren = GerenciadorViagens()
    opcao = 0

    while (opcao != "4"):
        print("\nO que deseja fazer?\n\n")

        print("1. Comprar uma passagem\n")
        print("2. Cancelar uma compra\n")
        print("3. Verificar passagens compradas\n")
        print("4. Sair\n\n")
        
        opcao = input("")

        while (opcao not in lista_opcoes):
            opcao = input("Por favor selecione uma opcao valida: ")

        if (opcao == "1"):
            print("Trechos disponíveis:\n")
            for chave, valor in geren.trechos.items():
                print(f"Trecho {chave} => {valor.trecho}")
                print(f"Assentos disponíveis => {valor.ASSENTOS}\n")

            print("Para escolher um trecho digite seu número correspondente:\n")
            opcao_trecho = input("")
            while opcao_trecho not in lista_opcoes_trecho:
                opcao_trecho = input("\nOpcao invalida => Escolha uma nova:")

            #Para confirmar que escolheu certo
            print("O TRECHO ESCOLHIDO FOI:\n")
            print(f"{geren.trechos[opcao_trecho]}")
            print("\n =-=- Deseja confirmar a compra? =-=-\n(1) SIM\n(2) NAO\n")
            opcao_confirma_compra = input("")
            if opcao_confirma_compra == "1":
                pass
                # processo de compra
            else:
               pass
                # sair

            # perguntar o local de partida + 'if' de nao achado
            # perguntar o local de chegada + 'if' de nao achado
            # juntarInformacoes
            # mandar a solicitacao para o servidor
            # pegar a resposta do servidor
        elif (opcao == "2"):
            pass
            # mostrar uma lista de passagens associadas ao usuario
            # pedir o 'ID' da passagem selecionada
            # juntarInformacoes
            # enviar a solicitacao para o servidor
            # pegar a resposta do servidor
        elif (opcao == "3"):
            pass
            # mostrar uma lista de passagens associadas ao usuario
            # pedir o 'ID' da passagem selecionada
            # juntarInformacoes
            # enviar a solicitacao para o servidor
            # pegar a resposta do servidor

mostrarMenu()
