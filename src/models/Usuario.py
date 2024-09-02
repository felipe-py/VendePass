import json
arquivo = "src/dados/usuarios.json"

class Usuario:
    def __init__(self, id, senha, viagens):
        self.id = id
        self.senha = senha
        self.viagens = viagens
        
    def exibir_info(self):
        # Método para exibir informações do usuário
        print(f"ID: {self.id}")
        
    def login(self, id, senha):
        # Método para validar a senha
        if self.senha == senha and self.id == id:
            return True
        
    def adicionar_viagem(self, destino):
        # Método para adicionar uma nova viagem à lista
        self.viagens.append(destino)
        print(f"Viagem para {destino} adicionada com sucesso.")
    
    def exibir_viagens(self):
        # Método para exibir todas as viagens do usuário
        if self.viagens:
            print(f"Viagens feitas por {self.id}:")
            for viagem in self.viagens:
                print(f"- {viagem}")
        else:
            print(f"{self.id} ainda não fez nenhuma viagem.")
            
    # Método para converter o objeto Usuario em um dicionário
    def to_dict(self):
        return {
            "ID": self.id,
            "senha": self.senha,  # Armazenando a senha como parte do dicionário
        }

    # Método estático para criar um objeto Usuario a partir de um dicionário
    @staticmethod
    def from_dict(data):
        usuario = Usuario(data["id"], data["senha"], data["senha"])
        return usuario
    
    # Função para salvar uma lista de usuários em um arquivo JSON
    @staticmethod
    def salvar_usuario(usuario):
        try:
            # Carregar os usuários existentes
            with open(arquivo, 'r') as f:
                # Verificar se o arquivo está vazio
                content = f.read().strip()
                if content:
                    usuarios_existentes = json.loads(content)
                else:
                    usuarios_existentes = []
        except FileNotFoundError:
            # Se o arquivo não existir, começamos com uma lista vazia
            usuarios_existentes = []

        # Adicionar o novo usuário
        usuarios_existentes.append(usuario.to_dict())

        # Salvar todos os usuários de volta no arquivo
        with open(arquivo, 'w') as f:
            json.dump(usuarios_existentes, f, indent=4)

        print(f"Usuário salvo em {arquivo}.")

    # Função para carregar usuários de um arquivo JSON
    def carregar_usuarios(arquivo):
        try:
            with open(arquivo, 'r') as f:
                dados = json.load(f)
                return [Usuario.from_dict(usuario) for usuario in dados]
        except FileNotFoundError:
            print(f"Arquivo {arquivo} não encontrado.")
            return []
        