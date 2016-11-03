from plasta.logic.manager import BaseManager
from renglon import Renglon

class RenglonManager( BaseManager ):
    
    def __init__(self, store, reset = False ):        
        BaseManager.__init__(self, store, reset)
        self.CLASS = Renglon
        self._operaciones_de_inicio()
        
    def obtenerRenglonesVenta(self, venta):
        return [obj for obj in self.almacen.find(Renglon, Renglon.venta_id == venta.ide)]
