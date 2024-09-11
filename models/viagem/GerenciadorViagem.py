import json
from models.viagem.Rota import Rota
arquivo_json = "dados/rotas.json"

class GerenciadorViagens:
    def __init__(self):
        self.trechos = self.ler_json()

    def __str__(self):
        if not self.trechos:
            return "Nenhum trecho disponível."

        resultado = "Trechos disponíveis:\n"
        for key, rota in self.trechos.items():
            resultado += f"Trecho: {key}, Destino: {rota.trecho}, Assentos Disponíveis: {rota.numeroAssentos}\n"
        return resultado

    def ler_json(self):
        try:
            with open(arquivo_json, 'r') as arquivo:
                dados = json.load(arquivo)
                return {k: Rota(v["trecho"]) for k, v in dados.items()}
        except FileNotFoundError:
            return {}

    def escrever_json(self):
        dados = {k: {"trecho": v.trecho, "assentos_disponiveis": v.numeroAssentos} for k, v in self.trechos.items()}
        with open(arquivo_json, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)

    def aumentar_assentos(self, trecho_key):
        if trecho_key in self.trechos:
            self.trechos[trecho_key].aumentarAssento()
            self.escrever_json()
        else:
            print(f"Trecho {trecho_key} não encontrado.")

    def diminuir_assentos(self, trecho_key):
        if trecho_key in self.trechos:
            self.trechos[trecho_key].diminuirAssento()
            self.escrever_json()
        else:
            print(f"Trecho {trecho_key} não encontrado.")

    def adicionar_trecho(self, trecho_key, trecho):
        if trecho_key not in self.trechos:
            self.trechos[trecho_key] = Rota(trecho)
            self.escrever_json()
        else:
            print(f"Trecho {trecho_key} já existe.")

    def remover_trecho(self, trecho_key):
        if trecho_key in self.trechos:
            del self.trechos[trecho_key]
            self.escrever_json()
        else:
            print(f"Trecho {trecho_key} não encontrado.")
    
    def realizar_viagem(self, trecho_key):
        if trecho_key in self.trechos:
            self.trechos[trecho_key].finalizarRota()
            self.escrever_json()
        else:
            print(f"Trecho {trecho_key} não encontrado.")
            