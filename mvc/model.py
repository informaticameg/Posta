#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setting.manager import SettingManager
from producto.manager import ProductoManager
from categoria.manager import CategoriaManager
from venta.manager import VentasManager
from renglon.manager import RenglonManager
from entrada.manager import EntradaManager
from salida.manager import SalidaManager
from resumen.manager import ResumenManager

class Models(object):

    def __init__(self, controller):
        self.controller = controller        
        almacen = controller.almacen
        reset_value = not controller.dbExist

        self.setting = SettingManager(almacen, reset = reset_value)
        self.productos = ProductoManager(almacen, reset = reset_value)
        self.categorias = CategoriaManager(almacen, reset = reset_value)
        self.renglones = RenglonManager(almacen, reset = reset_value)
        self.ventas = VentasManager(almacen, self.renglones, reset = reset_value)
        self.entradas = EntradaManager(almacen, reset = reset_value)
        self.salidas = SalidaManager(almacen, reset = reset_value)
        self.resumen = ResumenManager(almacen, reset_value, managers = [
            self.ventas, self.entradas, self.salidas
        ])
        
