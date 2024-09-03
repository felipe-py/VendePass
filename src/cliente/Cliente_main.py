import json
arquivo_usuarios = "src/dados/usuarios.json"

class Usuario:
    def __init__(self, id, senha):
        self.id = id
        self.senha = senha
            
    def __str__(self):
        return f"Usuário(id={self.id})"
        
    def login(self, id, senha):
        # Método para validar a senha
        if self.senha == senha and self.id == id:
            return True
            
    # Método para converter o objeto Usuario em um dicionário
    def to_dict(self):
        return {
            "id": self.id,
            "senha": self.senha,
        }

    # Método estático para criar um objeto Usuario a partir de um dicionário
    @staticmethod
    def from_dict(data):
        usuario = Usuario(data["id"], data["senha"])
        return usuario
    
    # Função para salvar uma lista de usuários em um arquivo JSON
    @staticmethod
    def salvar_usuario(usuario):
        try:
            # Carregar os usuários existentes
            with open(arquivo_usuarios, 'r') as f:
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
        with open(arquivo_usuarios, 'w') as f:
            json.dump(usuarios_existentes, f, indent=4)

        print(f"Usuário salvo em {arquivo_usuarios}.")

    # Função para carregar usuários de um arquivo JSON
    @staticmethod
    def carregar_usuarios():
        try:
            with open(arquivo_usuarios, 'r') as f:
                dados = json.load(f)
                return [Usuario.from_dict(usuario) for usuario in dados]
        except FileNotFoundError:
            print(f"Arquivo {arquivo_usuarios} não encontrado.")
            return []
    
        