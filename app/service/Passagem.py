#from dataclasses import dataclass
from DateTime import date

class Passagem:
    def __init__(self, dataCompra, reserva, cidadeSaida, cidadeChegada, poltrona, estaPago, estaCancelado):
        self.dataCompra    = dataCompra
        self.reserva       = reserva
        self.cidadeSaida   = cidadeSaida
        self.cidadeChegada = cidadeChegada
        self.poltrona      = poltrona  # Retirar depois
        self.estaPago      = estaPago
        self.estaCancelado = estaCancelado
    
    def realizarCompra(self):
        
        return
    def realizarReserva(self):
        
        return
    def realizarPagamento(self):
        
        return
    def realizarCancelamento(self):
        
        return
