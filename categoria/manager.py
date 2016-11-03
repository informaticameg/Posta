from plasta.logic.manager import BaseManager
from categoria import Categoria

class CategoriaManager( BaseManager ):
    
    def __init__(self, store, reset = False ):        
        BaseManager.__init__(self, store, reset)
        self.CLASS = Categoria
        self._operaciones_de_inicio()

    def obtenerPorNombre(self, nombre):
        resultado = [obj for obj in self.almacen.find(self.CLASS, Categoria.nombre == nombre)]
        return resultado[0] if resultado else None