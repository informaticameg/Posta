#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from categoria import Categoria
from os.path import join,abspath,dirname 
from PyQt4 import QtCore, QtGui, uic
import GUI.images_rc
from datetime import datetime
from venta import Venta
from renglon import Renglon 
from plasta.gui.mytablewidget import MyTableWidget

class Ventas( BaseGUI ):

    def __init__(self, parent, manager, managers = []):
        BaseGUI.__init__(self, parent, manager, managers)
        
        self.DialogAddClass = None
        self.setWindowIcon(QtGui.QIcon(':/newPrefix/cart.png'))
        self.FILENAME = 'pos/ventas.ui'
        self.ALINEACIONLISTA = ['C','C','C']
        
        self.ATRIBUTOSLISTA = [ 
        {u' ':Venta.ide},
        {u'Fecha y hora':Venta.fecha},
        {u'Total':Venta.total}
        ]
        self.renglonesManager = managers[0]
        self._operaciones_de_inicio()
        
        self.deFecha.setDate(datetime.today())
        self.makeTableDetalle()
        
        ventas = self.manager.obtenerVentas(self.deFecha.date().toPyDate())
        self.cargarTabla(ventas)
        
    def _operaciones_de_inicio(self):
        self.loadUi()
        self.setWindowTitle("Detalles de ventas")
        self._makeTable()
        self._loadAppShortcuts()
        self.fullScreen = False
        self._centerOnScreen()
        
    def _obtenerValoresAtributos(self,obj):
        resultado = []
        atributos_objeto = self.manager.getClassAttributesValues(obj)
        if not self.ATRIBUTOSLISTA :            
            return atributos_objeto
        else:
            atributos_clase = self.manager.getClassAttributes()
            atributos_ordenados = self.ATRIBUTOSLISTA_CLASSNAMES
            for atributo in atributos_ordenados:
                resultado.append( atributos_objeto[ atributos_clase.index( atributo ) ] )
            resultado[1] = resultado[1].strftime('%d/%m/%Y %H:%M')
            resultado[2] = "$ %8.2f" % float(resultado[2])
            return resultado
        
    def makeTableDetalle(self):
        self.getAtributosListaDetalle()
        columnasTablas = [p.keys()[0] for p in self.ATRIBUTOSLISTA_DETALLE]
        self.tablaDetalle = MyTableWidget(self.twDetalle, columnasTablas, ['C','L','C','C'])
        
    def getAtributosListaVenta(self):
        self.ATRIBUTOSLISTA = [ 
        {u' ':Venta.ide},
        {u'Fecha y hora':Venta.fecha},
        {u'Total':Venta.total}
        ]
        
    def getAtributosListaDetalle(self):
        self.ATRIBUTOSLISTA_DETALLE = [ 
        {u'Cantidad':Renglon.prod_cant},
        {u'Descripcion':Renglon.prod_descripcion},
        {u'Precio':Renglon.prod_precio},
        {u'Importe':Renglon.prod_precio}
        ]
        
    def _itemTableSelected(self):
        venta = self.actual_rows_to_objects()
        if venta:
            venta = venta[0]
            renglones = self.renglonesManager.obtenerRenglonesVenta(venta)
            items = []
            self.lbTotal.setText("$ %8.2f" % venta.total)
            self.lbPagoCon.setText("$ %8.2f" % venta.paga_con)
            for renglon in renglones:
                importe = float(renglon.prod_cant) * float(renglon.prod_precio)
                items.append([
                renglon.prod_cant,
                renglon.prod_descripcion,
                "$ %8.2f" % renglon.prod_precio,
                "$ %8.2f" % importe
                ])
            self.tablaDetalle.addItems(items)
            
    def on_deFecha_dateChanged(self , date):
        ventas = self.manager.obtenerVentas(date.toPyDate())
        self.cargarTabla(ventas)
        
    def on_twDatos_currentItemChanged(self , item_a, item_b):
        self._itemTableSelected()

    def on_twDatos_itemClicked(self , item):
        self._itemTableSelected()