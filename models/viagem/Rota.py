class Rota:
    
    ASSENTOS = 2
    def __init__(self, trecho):
        self.trecho = trecho
        self.numeroAssentos = self.ASSENTOS
    
    def diminuirAssento(self):
        self.numeroAssentos -= 1    
        return
    
    def aumentarAssento(self):
        self.numeroAssentos += 1
        return
    
    def finalizarRota(self):
        self.numeroAssentos = self.ASSENTOS
        return
    
    def __str__(self):
        return f"Rota: {self.trecho}, Assentos Disponíveis: {self.numeroAssentos}"
    