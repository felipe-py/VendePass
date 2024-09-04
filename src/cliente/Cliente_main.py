import json
arquivo_clientes = "src/dados/clientes.json"

class Cliente:
    def __init__(self, id, senha):
        self.id = id
        self.senha = senha
            
    def __str__(self):
        return f"Usuário(id={self.id})"
        
    def login(self, id, senha):
        if self.senha == senha and self.id == id:
            return True
            
    # Método para converter o objeto cliente em um dicionário
    def to_dict(self):
        return {
            "id": self.id,
            "senha": self.senha,
        }

    # Método estático para criar um objeto cliente a partir de um dicionário
    @staticmethod
    def from_dict(data):
        cliente = Cliente(data["id"], data["senha"])
        return cliente
    
    # Função para salvar uma lista de usuários em um arquivo JSON
    @staticmethod
    def salvar_cliente(cliente):
        try:
            # Carregar os usuários existentes
            with open(arquivo_clientes, 'r') as f:
                # Verificar se o arquivo está vazio
                content = f.read().strip()
                if content:
                    clientes_existentes = json.loads(content)
                else:
                    clientes_existentes = []
        except FileNotFoundError:
        # Se o arquivo não existir, começamos com uma lista vazia
            clientes_existentes = []
        
        # Adicionar o novo usuário
        clientes_existentes.append(cliente.to_dict())

        # Salvar todos os usuários de volta no arquivo
        with open(arquivo_clientes, 'w') as f:
            json.dump(clientes_existentes, f, indent=4)

        print(f"Usuário salvo em {arquivo_clientes}.")

    # Função para carregar usuários de um arquivo JSON
    @staticmethod
    def carregar_clientes():
        try:
            with open(arquivo_clientes, 'r') as f:
                dados = json.load(f)
                return [Cliente.from_dict(cliente) for cliente in dados]
        except FileNotFoundError:
            print(f"Arquivo {arquivo_clientes} não encontrado.")
            return []
    
        