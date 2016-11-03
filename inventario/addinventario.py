from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic, QtGui, QtCore
from os.path import join,abspath,dirname 
import GUI.images_rc

class AddInventario( BaseAddWindow ):

    def __init__(self, parent, unManager, itemaeditar = False, managers = []):
        BaseAddWindow.__init__(self, parent, unManager, itemaeditar, managers)
        self.FILENAME = 'inventario/agregarinventario.ui'
        self.loadUi()
        self.setWindowIcon(QtGui.QIcon(':newPrefix/desktop_icon/posta_icon_128.png'))
        self.postMethod = None

        self.lbProducto.setText(itemaeditar.descripcion)
        self.lbCantidad.setText(str(itemaeditar.cantidad))
        self.setWindowTitle("Agregar inventario al producto seleccionado")

    @QtCore.pyqtSlot()
    def on_btGuardar_clicked(self):
        value = self.sbCantidad.value()
        self.EDITITEM.cantidad = int(self.EDITITEM.cantidad) + value
        self.manager.almacen.commit()
        self.postMethod()
        self.close()
