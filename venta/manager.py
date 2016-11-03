from plasta.logic.manager import BaseManager
from venta import Venta
from renglon import Renglon 

class VentasManager( BaseManager ):
    
    def __init__(self, store, rm, reset = False ):        
        BaseManager.__init__(self, store, reset)
        self.CLASS = Venta
        self._operaciones_de_inicio()
        self.renglonManager = rm
        self.renglones = []
    
    def obtenerCantidadProducto(self, producto):
        ''' Devuelve la cantidad agregada en el ticket para un producto. '''
        try:
            return self.renglones[self.productosActuales().index(producto)][1]
        except ValueError:
            return 0
        
    def obtenerCantidadProductos(self):
        ''' Devuelve la cantidad total de productos agregados en el ticket. '''
        return sum([r[1] for r in self.renglones])
        
    def productosActuales(self):
        return [r[0] for r in self.renglones]
        
    def obtenerRenglon(self, index):
        return self.renglones[index]
        
    def obtenerRenglones(self):
        return self.renglones
        
    def agregarRenglon(self, producto):
        
        if producto not in self.productosActuales():
            self.renglones.append([producto,1]) 
        else:
            cantidad_actual = self.obtenerCantidadProducto(producto)
            self.cambiarCantidadProducto(producto, cantidad_actual + 1)

    def quitarRenglon(self, producto):
        index = self.productosActuales().index(producto)
        del self.renglones[index]

    def obtenerTotal(self):
        total = 0
        for producto in self.productosActuales() :
            cantidad = self.obtenerCantidadProducto(producto)
            total += producto.precio_venta * cantidad
        return total
    
    def cambiarCantidadProducto(self, producto, cantidad):
        self.renglones[self.productosActuales().index(producto)][1] = cantidad
        
    def confirmarVenta(self, paga_con, tipo_venta):
        total = self.obtenerTotal()
        # crea el objeto para la actual venta
        unaVenta = self.almacen.add( Venta(total, paga_con, tipo_venta) )
        obj_renglones = []
        try:
            # crea los objetos para cada uno 
            # de los renglones de la venta
            from renglon import Renglon
            for producto in self.productosActuales() :
                cantidad = self.obtenerCantidadProducto(producto)

                # descuenta del stock del producto la cantidad actual
                # si este producto utiliza inventario
                if producto.usa_inventario : 
                    producto.cantidad -= cantidad
                    self.almacen.commit()
                # crea el objeto renglon 
                renglon = [
                    unaVenta,
                    producto.descripcion,
                    producto.precio_venta,
                    cantidad
                ]
                unRenglon = self.renglonManager.add( *renglon )
                obj_renglones.append( unRenglon )
            # almacena los objetos
            self.almacen.flush()
            self.almacen.commit()
            print 'Venta realizada satisfactoriamente...'
            self.renglones = []
            return True
        except Exception, msg:
            print 'confirmarVenta() > ', msg
            self.almacen.remove( unaVenta )
            [self.almacen.remove( renglon ) for renglon in obj_renglones]
            return False

    def cancelarVenta(self):
        self.renglones = []

    def obtenerVentas(self, _fecha):
        return self.__getByFecha(self.getall(), _fecha)
       
    def __getByFecha(self, objs, fecha):
        return [obj 
            for obj in objs
                if obj.fecha.year == fecha.year and 
                obj.fecha.month == fecha.month and 
                obj.fecha.day == fecha.day]     
