#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import *
from venta import Venta

class Renglon (object):
    
    __storm_table__ = "Renglon"

    ide = Int(primary = True)
    venta_id = Int()
    venta = Reference(venta_id, Venta.ide)
    prod_descripcion = Unicode()
    prod_precio = Float()    
    prod_cant = Int()
    
    def __init__(self, venta, desc, precio, cant):
        self.venta = venta
        self.prod_descripcion = desc
        self.prod_precio = precio
        self.prod_cant = cant
        
