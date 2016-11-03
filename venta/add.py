from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic, QtGui
from os.path import join,abspath,dirname 
from venta import Venta

class AddVenta( BaseAddWindow ):

    def __init__(self, parent, unManager, itemaeditar = False, managers = []):
        BaseAddWindow.__init__(self, parent, unManager, itemaeditar, managers)
        self.FILENAME = 'venta/agregar.ui'
        self.loadUi()
        self.setWindowIcon(QtGui.QIcon(':/newPrefix/logo.png'))
        self.ITEMLIST = [
        ]
        self._operaciones_de_inicio()
