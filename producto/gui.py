#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from GUI.mtw_pos import MyTableWidget
from producto import Producto
from producto.add import AddProducto
from os.path import join,abspath,dirname 
from PyQt4 import QtCore, QtGui, uic
import GUI.images_rc
import locale

class ProductoGUI( BaseGUI ):

    def __init__(self, parent, manager, managers = []):
        BaseGUI.__init__(self, parent, manager, managers)
        
        locale.setlocale( locale.LC_ALL, '' )
        self.DialogAddClass  = AddProducto
        self.setWindowIcon(QtGui.QIcon(':/newPrefix/logo.png'))
        self.FILENAME = 'producto/admin.ui'
        self.ALINEACIONLISTA = ['C','L','L','C','C','C','C']
        self.ATRI_COMBO_BUSQUEDA = [
        {u'Codigo':Producto.codigo},
        {u'Descripcion del producto':Producto.descripcion},
        {u'Precio venta':Producto.precio_venta},
        {u'Existencia':Producto.cantidad},
        {u'Inv. Minimo':Producto.minimo},
        ]
#~ 
        self.ATRIBUTOSLISTA = [ 
        {u'Codigo':Producto.codigo},
        {u'Categoria':Producto.categoria},
        {u'Descripcion del producto':Producto.descripcion},
        {u'Precio costo':Producto.precio_costo},
        {u'Precio venta':Producto.precio_venta},
        {u'Existencia':Producto.cantidad},
        {u'Inv. Minimo':Producto.minimo},
        ]
        self._operaciones_de_inicio()
        self.setWindowTitle("Productos")

    def _operaciones_de_inicio(self):
        self.loadUi()

        self.setWindowTitle(self.TITULO)
        self.lbTitulo.setText(self.manager.getClassName())