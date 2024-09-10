#from dataclasses import dataclass
from datetime import date

class Rota:
    def __init__(self, cidadeSaida, cidadeChegada, data, numeroAssentos):
        self.cidadeSaida      = cidadeSaida
        self.cidadeChegada    = cidadeChegada
        self.data             = data            # Temos que dar um jeito de passar a data pro objeto...
        self.numeroAssentos   = numeroAssentos
        self.vendasPermitidas = 1              # Depois que a viagem ja aconteceu, ou se for cancelada, devemos impedir futuras operações
    
    def diminuirAssento(self):
        self.numeroAssentos =-1    
        return
    
    def aumentarAssento(self):
        self.numeroAssentos =+ 1
        return
    
    def finalizarRota(self):
        self.vendasPermitidas = 0
        return
    
    def reabrirRota(self):
        self.vendasPermitidas = 1
        return

