#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic, QtGui,QtCore
from os.path import join,abspath,dirname 
from salida import Salida 
import GUI.images_rc

class AddSalida(BaseAddWindow):
    
    def __init__(self, parent, unManager, itemaeditar = False, managers = []):
        BaseAddWindow.__init__(self, parent, unManager, itemaeditar, managers)
        self.FILENAME = 'salida/salida.ui'
        self.loadUi()
        self.setWindowIcon(QtGui.QIcon(':/newPrefix/forward.png'))
        self.ITEMLIST = [
             {self.dsbMonto:Salida.monto},
             {self.teMotivo:Salida.motivo},
             {self.leProducto:Salida.producto_nombre},
             {self.sbCantidad:Salida.producto_cantidad},
        ]
        self._operaciones_de_inicio()
        self.setWindowTitle("Registrar una salida de dinero")
        self.tabWidget.removeTab(1)
        self.dsbMonto.setFocus()

    @QtCore.pyqtSlot()
    def on_btGuardar_clicked(self):
        if self.dsbMonto.value() > 0.0 :
            BaseAddWindow.on_btGuardar_clicked(self)