#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic, QtGui,QtCore
from os.path import join,abspath,dirname 
from entrada import Entrada
import GUI.images_rc

class AddEntrada(BaseAddWindow):
    
    def __init__(self, parent, unManager, itemaeditar = False, managers = []):
        BaseAddWindow.__init__(self, parent, unManager, itemaeditar, managers)
        self.FILENAME = 'entrada/entrada.ui'
        self.loadUi()
        self.setWindowIcon(QtGui.QIcon(':/newPrefix/back.png'))
        self.ITEMLIST = [
             {self.dsbMonto:Entrada.monto},
             {self.teMotivo:Entrada.motivo}
        ]
        self._operaciones_de_inicio()
        self.setWindowTitle("Registrar una entrada de dinero")

    @QtCore.pyqtSlot()
    def on_btGuardar_clicked(self):
        if self.dsbMonto.value() > 0.0 :
            BaseAddWindow.on_btGuardar_clicked(self)