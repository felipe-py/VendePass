class Usuario:
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha
        self.passagens = []

    def entrar(self, login, senha):
        if (self.login==login and self.senha == senha):
            print(f'logado com sucesso {login}')
        else:
            print(f'Não foi possivel logar, tente novamente')

    def adicionarPassagem(self, passagem):
        self.passagens.append(passagem)
