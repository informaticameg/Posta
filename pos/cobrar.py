#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Informática MEG <contacto@informaticameg.com>
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

import os, sys, cStringIO
from PyQt4 import QtCore, QtGui, uic
# import GUI.images_rc

class Cobrar(QtGui.QDialog):

    def __init__(self, parent, vm):
        self.parent = parent
        self.FILENAME = 'pos/cobrar.ui'
        QtGui.QDialog.__init__(self)
        UI_CONTENT = cStringIO.StringIO(self.parent.parent.uis[self.FILENAME])
        uic.loadUi(UI_CONTENT, self)
        self.__centerOnScreen()

        self.ventasManager = vm
        self.total = self.ventasManager.obtenerTotal()
        self.lbTotal.setText("$ %8.2f" % self.total)

        QtGui.QShortcut(QtGui.QKeySequence("F12"), self, self.on_btCobrar_clicked)
        QtGui.QShortcut(QtGui.QKeySequence("F10"), self, self.on_btAutoconsumo_clicked)
        self.setWindowTitle("Cobrar venta")
        self.setWindowIcon(self.parent.windowIcon())
        self.dsbPagaCon.setValue(self.total)
        self.dsbPagaCon.setFocus()
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)

    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    @QtCore.pyqtSlot()
    def on_btCancelar_clicked(self):
        self.close()

    @QtCore.pyqtSlot()
    def on_btCobrar_clicked(self):
        paga_con = self.dsbPagaCon.value()
        if paga_con >= self.total:
            tipo_venta = u'efectivo'
            self.ventasManager.confirmarVenta(paga_con, tipo_venta)
            self.parent.reestablecerCampos()
            self.close()
        else:
            QtGui.QMessageBox.warning(self, "Cobrar venta",
        "El monto a pagar no puede ser menor que el total de la venta.")
            self.dsbPagaCon.setFocus()

    @QtCore.pyqtSlot(float)
    def on_dsbPagaCon_valueChanged(self, value):
        self.lbCambio.setText("$ %8.2f" % (value - self.total))

    @QtCore.pyqtSlot()
    def on_btAutoconsumo_clicked(self):
        productos = self.ventasManager.obtenerRenglones()
        salidasManager = self.parent.managers[2].manager

        for prod, prod_cant in productos:
            new_salida = [0,u'',prod.descripcion, prod.precio_venta, prod_cant]
            salidasManager.add(*new_salida)
        QtGui.QMessageBox.information(self, "Cobrar venta",
            "Auto-consumo registrado correctamente.")
        self.ventasManager.cancelarVenta()
        self.parent.reestablecerCampos()
        self.close()

def main():
    app = QtGui.QApplication(sys.argv)
    window = Cobrar()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
