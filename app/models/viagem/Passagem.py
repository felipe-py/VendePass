
class Passagem:
    def __init__(self, reserva, cidadeSaida, cidadeChegada, estaPago, estaCancelado):
        self.reserva       = reserva
        self.cidadeSaida   = cidadeSaida
        self.cidadeChegada = cidadeChegada
        self.estaPago      = estaPago
        self.estaCancelado = estaCancelado
    
    def realizarPagamento():
        self.estaPago = True
        return

    def realizarCancelamento():
        self.estaCancelado = True
        return

    def desfazerCancelamento():
        self.estaCancelado = False
        return
