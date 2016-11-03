#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os, sys, os.path
import cStringIO
from PyQt4 import QtCore, QtGui, uic
import GUI.images_rc #@UnusedImport
from os.path import join,abspath,dirname

class AllModules(QtGui.QMainWindow):

    def __init__(self, views):
        QtGui.QMainWindow.__init__(self)

        FILENAME = 'GUI/all_modules.ui'
        UI_CONTENT = cStringIO.StringIO(views.uis[FILENAME])
        uic.loadUi(UI_CONTENT, self)

        self.__centerOnScreen()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle("P.O.S.T.A.")
        self.setWindowIcon(QtGui.QIcon(':newPrefix/desktop_icon/posta_icon_128.png'))
        self.views = views

        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL+QtCore.Qt.Key_O), self, self.views.instanceSettingGUI)

        self.btSistema.setVisible(False)
        self.btClientes.setVisible(False)
        self.btProveedores.setVisible(False)
        self.createMenu()

    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def createMenu(self):
        menu = QtGui.QMenu(self.btMenu)
        #menu.addAction("Informar sobre un problema", self.views.instanceInformarProblema)
        #menu.addAction(u"Envíanos una sugerencia", self.views.instanceEnviarSugerencia)
        #menu.addAction(u"Opciones...", self.views.instanceSettingGUI)
        menu.addSeparator()
        menu.addAction("Acerca de POSTA", self.on_btAcercade_clicked)
        self.btMenu.setMenu(menu)

    @QtCore.pyqtSlot()
    def on_btXXX_clicked(self):
        pass

    @QtCore.pyqtSlot()
    def on_btCategorias_clicked(self):
        self.views.instanceCategoriasGUI()
        self.views.categorias.setWindowIcon( self.btCategorias.icon() )
        self.views.categorias.show()

    @QtCore.pyqtSlot()
    def on_btClientes_clicked(self):
        self.views.instanceClientesGUI()
        self.views.clientes.setWindowIcon( self.btClientes.icon() )
        self.views.clientes.show()

    @QtCore.pyqtSlot()
    def on_btInventario_clicked(self):
        self.views.instanceInventarioGUI(self)
        self.views.inventario.setWindowIcon( self.btInventario.icon() )
        self.views.inventario.show()

    @QtCore.pyqtSlot()
    def on_btResumenes_clicked(self):
        self.views.instanceResumenesGUI()
        self.views.resumen.setWindowIcon( self.btResumenes.icon() )
        self.views.resumen.show()

    @QtCore.pyqtSlot()
    def on_btSistema_clicked(self):
        self.views.instanceSistema()
        self.views.sistema.setWindowIcon( self.btSistema.icon() )
        self.views.sistema.show()

    @QtCore.pyqtSlot()
    def on_btAcercade_clicked(self):
        self.views.instanceAcercaDe()
        self.views.acercade.show()

    @QtCore.pyqtSlot()
    def on_btPOS_clicked(self):
        cantProds = len(self.views.managers.productos.getall())
        if cantProds > 0 :
            self.views.instancePOS(self)
            self.views.pos.setWindowIcon( self.btPOS.icon() )
            self.views.pos.show()
        else:
            QtGui.QMessageBox.information(self, "P.O.S.T.A.",u"No se han cargado productos para vender todavía.")

    def close(self, event = None):
        sys.exit(0)
