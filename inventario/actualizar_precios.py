#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
from PyQt4 import QtCore, QtGui, uic
import GUI.images_rc #@UnusedImport
import tools.pathtools, cStringIO

class ActualizarPrecios(QtGui.QDialog):
    
    def __init__(self, parent):
        self.parent = parent
        self.FILENAME = 'inventario/actualizarprecios.ui'
        QtGui.QDialog.__init__(self)
        #UI_CONTENT = cStringIO.StringIO(self.parent.parent.uis[self.FILENAME])
        #uic.loadUi(UI_CONTENT, self)
        uic.loadUi(self.FILENAME, self)
        
        self.__centerOnScreen()
        
        self.manager = parent.manager
        self.almacen = parent.manager.almacen
        self.title = "Actualizar precios"

        self.widgetProgreso.setVisible(False)
        self.setWindowIcon(QtGui.QIcon(':newPrefix/computer.png'))
        self.setWindowTitle(self.title)

        self.cargarComboCategorias()
        
    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def cargarComboCategorias(self):
        categorias = self.parent.managers[1].manager.getall()
        self.cbCategorias.addItem(u'TODAS')
        self.cbCategorias.addItem(u'SIN CATEGORIA')
        categorias = [categoria.nombre for categoria in categorias]
        categorias.sort()
        [self.cbCategorias.addItem(cat) for cat in categorias]

    def _filtrarPorCategoria(self, value):        
        productos = []
        if value != u'TODAS' and value != u'SIN CATEGORIA':
            categoriasManager = self.managers[1].manager
            unaCategoria = categoriasManager.obtenerPorNombre(value)
            productos = self.manager.obtenerPorCategoria(unaCategoria)
        elif value == u'SIN CATEGORIA':
            productos = self.manager.obtenerSinCategoria()
        else:
            productos = self.manager.allItems['data']
        return productos

    @QtCore.pyqtSlot()
    def on_btComenzar_clicked(self):
        categoria = unicode(
            self.cbCategorias.itemText(
                self.cbCategorias.currentIndex()).toUtf8(), 'utf-8')
        campo = self.cbCampo.currentIndex()
        productos = self.parent._filtrarPorCategoria(categoria)
        porcentaje = self.sbPorcentaje.value()
        print porcentaje
        if len(productos) == 0:
            QtGui.QMessageBox.warning(
                self, 
                self.title,
                u"No hay productos para actualizar en la categoría seleccionada.")
        elif porcentaje == 0:
            QtGui.QMessageBox.warning(
                self, 
                self.title,
                u"Debes indicar un porcentaje a aplicar.")
        else:
            self.cbCategorias.setEnabled(False)
            self.sbPorcentaje.setEnabled(False)
            self.btComenzar.setEnabled(False)
            self.widgetProgreso.setVisible(True)            
            
            i = 1
            self.widgetProgreso.setMinimum(i)
            self.widgetProgreso.setMaximum(len(productos) + 2)

            multiplicador = 1 + (porcentaje/100)
            print campo, multiplicador
            for prod in productos:
                if campo == 0: # costo y venta
                    prod.precio_costo = prod.precio_costo * multiplicador
                    prod.precio_venta = prod.precio_venta * multiplicador
                elif campo == 1: # costo
                    prod.precio_costo = prod.precio_costo * multiplicador
                elif campo == 2: # venta
                    prod.precio_venta = prod.precio_venta * multiplicador
                i += 1
                self.widgetProgreso.setValue(i)
            
            #self.almacen.flush()
            self.almacen.commit()
            i += 1
            self.widgetProgreso.setValue(i)

            self.parent.manager._aiGetAll()
            self.parent.manager._aiGenerateIndex()
            i += 1
            self.widgetProgreso.setValue(i)
            self.parent.recargarLista()
            
            QtGui.QMessageBox.information(self, self.title,
                u"Actualización de precios terminada con éxito.")
            self.close()
