#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import *
from categoria import Categoria


class Producto (object):
    
    __storm_table__ = "Producto"

    codigo = Unicode(primary = True)
    descripcion = Unicode(allow_none = False)
    precio_costo = Float(allow_none = False)
    precio_venta = Float(allow_none = False)
    usa_inventario = Bool()
    cantidad = Int()
    minimo = Int()
    categoria_id = Int()
    categoria = Reference(categoria_id, Categoria.ide)

    
    def __init__(self,  unCodigo, unaDesc, unprecio_costo, unPrecio_venta, UI, unCantidad, unMinimo, unCategoria):
        self.codigo = unCodigo
        self.precio_costo = unprecio_costo
        self.precio_venta = unPrecio_venta
        self.cantidad = unCantidad
        self.minimo = unMinimo
        self.categoria = unCategoria
        self.descripcion = unaDesc
        self.usa_inventario = UI

    def __str__(self):
        return self.descripcion
