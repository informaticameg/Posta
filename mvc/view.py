#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
import sys

import uis
from GUI.allmodules import AllModules
from producto.gui import ProductoGUI
from categoria.gui import CategoriaGUI
from inventario.gui import InventarioGUI
from resumen.gui import ResumenGUI
from entrada.gui import EntradaGUI
from salida.gui import SalidaGUI
from setting.gui import SettingGUI
from pos.gui import POS
import GUI.images_rc #@UnusedImport

class View :

    def __init__(self, models):
        self.models = models
        self.managers = models
        self.uis = uis.uis
        self.initOperations()

    def initOperations(self):
        app = QtGui.QApplication(sys.argv)
        # Create and display the splash screen
        splash_pix = QtGui.QPixmap(':newPrefix/logo/posta-logo.png')
        splash = QtGui.QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()

        app.processEvents()
        splash.showMessage(
            QtCore.QString(u'Iniciando aplicación...'),
            alignment=Qt.AlignHCenter | Qt.AlignBottom)

        # get and index products
        self.managers.productos._aiGetAll()
        self.managers.productos._aiGenerateIndex()

        try:
            window = AllModules( self )
            window.show()
            splash.finish(window)
            sys.exit(app.exec_())
        except Exception, e :
            print e
            QtGui.QMessageBox.critical(
                None, "POSTA",
                "Ha ocurrido un error en el programa.\n\nIntenta volver a abrirlo.")

    def internet_on(self):
      import socket
      try:
        host = socket.gethostbyname("www.google.com")
        s = socket.create_connection((host, 80), 2)
        return True
      except:
         pass
      return False

    def instanceProductosGUI(self):
        self.instanceCategoriasGUI()
        self.productos = ProductoGUI(
            parent = self,
            manager = self.managers.productos,
            managers = [self.categorias])
        return self.productos

    def instanceCategoriasGUI(self):
        self.categorias = CategoriaGUI(
            parent = self,
            manager = self.managers.categorias,
            managers = [])

    def instanceInventarioGUI(self, parent):
        self.instanceProductosGUI()
        self.instanceCategoriasGUI()
        self.inventario = InventarioGUI(
            parent = self,
            windowparent = parent,
            manager = self.managers.productos,
            managers = [self.productos, self.categorias])

    def instanceResumenesGUI(self):
        self.resumen = ResumenGUI(
            parent = self,
            manager = self.managers.resumen,
            managers = [
                self.managers.ventas,
                self.managers.renglones
            ])

    def instanceEntradasGUI(self):
        self.entradas = EntradaGUI(
            parent = self,
            manager = self.managers.entradas,
            managers = [])

    def instanceSalidasGUI(self):
        self.salidas = SalidaGUI(
            parent = self,
            manager = self.managers.salidas,
            managers = [self.instanceProductosGUI()])

    def instancePOS(self, parent):
        self.instanceEntradasGUI()
        self.instanceSalidasGUI()
        self.pos = POS(
            parent = self,
            windowparent = parent,
            manager = self.managers.productos,
            managers = [
                self.managers.ventas,
                self.entradas,
                self.salidas,
                self.managers.renglones
            ])

    def instanceAcercaDe(self):
        from acercade import AcercaDe
        self.acercade = AcercaDe(self, self.managers.setting.get())

    def instanceSettingGUI(self):
        self.setting = SettingGUI(self, None, None, self.managers.setting.get())
        self.setting.show()

def main():
    pass

if __name__ == "__main__":
    main()
