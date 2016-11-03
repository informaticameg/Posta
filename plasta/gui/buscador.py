#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2012 Fernandez, Emiliano <emilianohfernandez@gmail.com>
#       Copyright 2012 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
#
#       Informática MEG <contacto@informaticameg.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import sys
from os.path import join,abspath,dirname
from PyQt4 import QtCore, QtGui, uic
import uis.images_rc #@UnusedImport
from plasta.gui import BaseGUI

class BaseBuscador(QtGui.QDialog, BaseGUI):

    def __init__(self,manager, dict_referencias = None):
        QtGui.QDialog.__init__(self)        
        FILENAME = 'uis/buscador.ui'
        uic.loadUi(join(abspath(dirname(__file__)),FILENAME), self)
        
        self.ATRI_COMBO_BUSQUEDA = []#el orden y la cantidad de atributos en str que quieras
        self.ATRIBUTOSLISTA = []#el orden y la cantidad de atributos en str que quieras
        self.ALINEACIONLISTA = []
        self.ATRIBUTOSLISTA_CLASSNAMES = []
        self.manager = manager
        self.dict_referencias = dict_referencias
        self.objetoSeleccionado = None
        self._operaciones_de_inicio()
        
    @QtCore.pyqtSlot()
    def on_btAceptar_clicked(self):
        objeto = self.actual_rows_to_objects()[0]
        if self.dict_referencias :
            clave = [k for k, v in self.dict_referencias.iteritems() if v == None][0]
            self.dict_referencias[clave] = objeto
            clave.setText(objeto.__str__())
        else:
            self.objetoSeleccionado = objeto            
        self.close()
    
    def on_twDatos_doubleClicked(self , index):
        self.on_btAceptar_clicked()
    
    #===================================================================
    # Metodos de Logica
    #===================================================================
    
    def _operaciones_de_inicio(self):
        u'''
        operaciones necesarias para levantar las ventanas
        '''
        self.lbTitulo.setText(self.manager.getClassName())
        self._makeTable()
        self.cargarCombobox()
        self.cargarTabla()
        self._loadAppShortcuts()
        self.fullScreen = False
        self._centerOnScreen()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)        
        
    def _loadAppShortcuts(self):
        u""" Load shortcuts used in the application. """
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)
        self._atajo_salir = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self, self.close)
        self._atajo_fullscreen = QtGui.QShortcut(QtGui.QKeySequence("F11"), self, self._toogleFullScreen)
        
def main():
    app = QtGui.QApplication(sys.argv)
    window = BaseBuscador()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
