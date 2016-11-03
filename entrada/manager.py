from plasta.logic.manager import BaseManager
from entrada import Entrada

class EntradaManager( BaseManager ):
    
    def __init__(self, store, reset = False ):        
        BaseManager.__init__(self, store, reset)
        self.CLASS = Entrada
        self._operaciones_de_inicio()

    def add(self,*params):
        '''
        Crea y agrega un objeto al almacen
        @param *params: los parametros que recibe el init de self.CLASS
        @return: true o false, dependiendo si se completo la operacion
        '''
        try:
            obj = self.CLASS(*params)
            self.almacen.add(obj)
            self.almacen.flush()
            self.almacen.commit()
            return True
        except Exception, e:
            print 'BaseManager.add() : ',self.CLASS, e
            return False
