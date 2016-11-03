from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic, QtGui, QtCore
from os.path import join,abspath,dirname 
from categoria import Categoria
import GUI.images_rc, cStringIO

class AddCategoria( BaseAddWindow ):

    def __init__(self, parent, unManager, itemaeditar = False, managers = []):
        BaseAddWindow.__init__(self, parent, unManager, itemaeditar, managers)
        self.FILENAME = 'categoria/agregar.ui'
        UI_CONTENT = cStringIO.StringIO(self.parent.uis[self.FILENAME])
        uic.loadUi(UI_CONTENT, self)
        
        self.setWindowIcon(QtGui.QIcon(':newPrefix/desktop_icon/posta_icon_128.png'))
        self.ITEMLIST = [
             {self.leNombre:Categoria.nombre},
        ]
        self._operaciones_de_inicio()
        self.leNombre.textEdited.connect(lambda text: self.leNombre.setText(text.toUpper()))
    
    @QtCore.pyqtSlot()
    def on_btGuardar_clicked(self):
        if not self.EDITITEM :
            value = unicode(self.leNombre.text().toUtf8(),'utf-8')
            if not self.manager.obtenerPorNombre(value):
                BaseAddWindow.on_btGuardar_clicked(self)
            else:
                QtGui.QMessageBox.warning(self, "Agregar categoria","Ya existe una categoria con este nombre.")
        else:
            BaseAddWindow.on_btGuardar_clicked(self)