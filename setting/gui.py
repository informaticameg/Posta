#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from os.path import join,abspath,dirname 
from PyQt4 import QtCore, QtGui

class SettingGUI( BaseGUI ):

    def __init__(self, parent, manager, managers = [], item = None):
        BaseGUI.__init__(self, parent, manager, managers)
        self.item = item
        self.setWindowIcon(QtGui.QIcon(':newPrefix/desktop_icon/posta_icon_128.png'))
        self.FILENAME = 'setting/gui.ui'
        self.develop = True
        self._operaciones_de_inicio()
        self.setWindowTitle(u"Opciones - P.O.S.T.A.")

    def _operaciones_de_inicio(self):
        self.loadUi()
        self.setWindowTitle(self.TITULO)
        self._loadAppShortcuts()
        self.fullScreen = False        
        self._centerOnScreen()

    def _loadAppShortcuts(self):
        self._atajo_salir = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self, self.close)
        self._atajo_fullscreen = QtGui.QShortcut(QtGui.QKeySequence("F11"), self, self._toogleFullScreen)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)

 
    @QtCore.pyqtSlot()
    def on_btPorcGanancia_clicked(self):
        QtGui.QMessageBox.information(
            self, "Porcentaje de ganancia",
            u"Este valor se usará para: \n\n" + \
            "- Calcular el precio de venta cuando no se haya indicado ninguno a partir del precio de costo.\n" + \
            "- Calcular el precio de costo cuando no se haya indicado ninguno a partir del precio de venta."
        )





