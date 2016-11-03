from plasta.logic.manager import BaseManager
from producto import Producto

class ProductoManager( BaseManager ):
    
    def __init__(self, store, reset = False ):        
        BaseManager.__init__(self, store, reset)
        self.CLASS = Producto
        self.allItems = {'data':None, 'index':{}}
        self._operaciones_de_inicio()

    ######################################################
    
    def _aiGetAll(self):
        print 'Iniciando carga desde BD...'
        self.allItems['data'] = self.getall()
        print 'Iniciando carga desde BD... OK'

    def _aiGenerateIndex(self):
        print 'Generando indices...'
        for index, producto in enumerate(self.allItems['data']):
            self.allItems['index'][producto.codigo] = index
        print 'Generando indices... OK'

    def _aiUpdateItem(self, codOld, obj):
        index = self.allItems['index'][codOld]
        if codOld != obj.codigo:
            del self.allItems['index'][codOld]
            self.allItems['index'][obj.codigo] = index
        self.allItems['data'][index] = obj

    def _aiDeleteItem(self, cod):
        index = self.allItems['index'][cod]
        del self.allItems['data'][index]
        self.allItems['index'] = {}
        self._aiGenerateIndex()

    def _aiAddItem(self, cod, obj):
        index = len(self.allItems['data'])
        self.allItems['data'].append(obj)
        self.allItems['index'][cod] = index

    def _aiGetCountAll(self):
        return len(self.allItems['data'])
        
    ######################################################

    def add(self,*params):
        try:
            obj = self.CLASS(*params)
            self.almacen.add(obj)
            self.almacen.flush()
            self.almacen.commit()
            self._aiAddItem(obj.codigo, obj)
            return True
        except Exception, e:
            print 'BaseManager.add() : ',self.CLASS, e
            return False
        
    def delete(self,obj):
        if isinstance(obj, self.CLASS):
            self.almacen.remove(obj)#where o is the object representing the row you want to remove
            self._aiDeleteItem(obj.codigo)
            del obj#lo sacamos de la ram
            self.almacen.commit()
            return True

    ######################################################

    def cantidadProductosBajosEnExistencia(self):
        return len([prod for prod in self.allItems['data'] if prod.cantidad < prod.minimo])

    def productosBajosEnStock(self):
        return [prod for prod in self.allItems['data'] if prod.cantidad < prod.minimo]

    def obtenerPorCategoria(self, categoria):
        return [obj for obj in self.allItems['data'] if obj.categoria == categoria] 

    def obtenerSinCategoria(self):
        return [obj for obj in self.allItems['data'] if obj.categoria == None]
        
    def existeProducto(self, codigo):
        return codigo in self.allItems['index'].keys()