from plasta.logic.manager import BaseManager
from salida import Salida

class SalidaManager( BaseManager ):
    
    def __init__(self, store, reset = False ):        
        BaseManager.__init__(self, store, reset)
        self.CLASS = Salida
        self._operaciones_de_inicio()
