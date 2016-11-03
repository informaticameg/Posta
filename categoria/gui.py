#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from categoria import Categoria
from categoria.add import AddCategoria
from os.path import join,abspath,dirname 
from PyQt4 import QtCore, QtGui
import GUI.images_rc

class CategoriaGUI( BaseGUI ):

    def __init__(self, parent, manager, managers = []):
        BaseGUI.__init__(self, parent, manager, managers)
        
        self.DialogAddClass  = AddCategoria
        self.setWindowIcon(QtGui.QIcon(':newPrefix/desktop_icon/posta_icon_128.png'))
        self.FILENAME = 'categoria/admin.ui'
        self.ALINEACIONLISTA = ['C','L']
        self.ATRI_COMBO_BUSQUEDA = [
        {u'Nombre':Categoria.nombre},
        ]
        

        self.ATRIBUTOSLISTA = [ 
        {u' ':Categoria.ide},
        {u'Nombre':Categoria.nombre},
        ]
        self._operaciones_de_inicio()
        self.setWindowTitle(u"Categorías - P.O.S.T.A.") 

    @QtCore.pyqtSlot()
    def on_btAgregar_clicked(self, postSaveMethod=None):
        wAgregar = self.agregar()
        if postSaveMethod:
            wAgregar.postSaveMethod = postSaveMethod
        else:
            wAgregar.postSaveMethod = self.recargarLista
        wAgregar.exec_()