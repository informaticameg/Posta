#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import *

class Salida (object):
    ''' Corresponde a una salida de dinero o productos'''
    
    __storm_table__ = "Salida"

    ide = Int(primary = True)
    fecha = DateTime()
    monto = Float()
    motivo = Unicode()
    tipo = Unicode() # dinero | producto | proveedor
    producto_nombre = Unicode()
    producto_precio = Float()
    producto_cantidad = Int() # cantidad del producto que salio
    
    def __init__(self, monto, motivo, prod_nombre = None, prod_precio = None, prod_cant = None):
        from datetime import datetime
        self.fecha = datetime.today()
        self.monto = monto
        self.motivo = motivo
        self.tipo = u'dinero'
        if prod_nombre is not None:
            self.tipo = u'producto'
            self.producto_nombre = prod_nombre
            self.producto_precio = prod_precio
            self.producto_cantidad = prod_cant
