#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from GUI.mtw_pos import MyTableWidget
from os.path import join,abspath,dirname 
from PyQt4 import QtCore, QtGui,uic
import GUI.images_rc
from producto import Producto

class POS ( BaseGUI ):

    ###
    ### BASE METODOS
    ###

    def __init__(self, parent, windowparent, manager, managers = []):
        BaseGUI.__init__(self, parent, manager, managers)        
        self.setWindowIcon(QtGui.QIcon(':newPrefix/desktop_icon/posta_icon_128.png'))
        self.FILENAME = 'pos/pos.ui'
        self.ATRI_COMBO_BUSQUEDA = [
        {u'DESCRIPCION':Producto.descripcion},
        {u'CODIGO':Producto.codigo}
        ]
        self.ALINEACIONLISTA = ['C','L','C','C']
        self.ALINEACIONLISTA_TICKET = ['C','C','L','C','C']
        self.ATRIBUTOSLISTA = [ 
        {u'Codigo':Producto.codigo},
        {u'Descripcion del producto':Producto.descripcion},
        #{u'Existencia':Producto.cantidad},
        {u'Precio':Producto.precio_venta},
        ]
        self.ATRIBUTOSLISTA_TICKET = [ 
        {u'Codigo':Producto.codigo},
        {u'Cantidad':Producto.codigo},
        {u'Descripcion del producto':Producto.descripcion},
        {u'Precio':Producto.precio_venta},
        {u'Subtotal':Producto.precio_venta},
        ]
        
        self.tablaTicket = None
        self.parent = parent
        self.windowparent = windowparent
        self._operaciones_de_inicio()     
        self.windowparent.hide()
        # managers instance
        self.ventasManager = managers[0]

    def _operaciones_de_inicio(self):
        u'''
        operaciones necesarias para levantar las ventanas
        '''
        self.loadUi()
        self._makeTable() # tabla busqueda
        self.makeTableTicket()
        
        self.cargarCombobox()
        self._loadAppShortcuts()
        self.menuMasAtajos()
        self.fullScreen = False
        self._centerOnScreen()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setWindowTitle("Punto de venta - P.O.S.T.A.")
        self.leBusqueda.setFocus()
    
    def _makeTable(self):
        if not self.ATRIBUTOSLISTA :
            columnasTablas = [p.capitalize() for p in self._obtener_atributos_names()]
        else:
            self.ATRIBUTOSLISTA_CLASSNAMES = [ self.manager.obtenerNombreAtributo( p.values()[0] ) for p in self.ATRIBUTOSLISTA]
            columnasTablas = [p.keys()[0] for p in self.ATRIBUTOSLISTA]
        self.MyTabla = MyTableWidget(self.twDatos, columnasTablas, self.ALINEACIONLISTA, indexColumn = 1, widthColumn = 600)

    def close(self):
        self.ventasManager.cancelarVenta()
        BaseGUI.close(self)
        self.windowparent.show()

    def _obtenerValoresAtributos(self,obj):
        resultado = []
        atributos_objeto = self.manager.getClassAttributesValues(obj)
        if not self.ATRIBUTOSLISTA :            
            return atributos_objeto
        else:
            atributos_clase = self.manager.getClassAttributes()
            atributos_ordenados = self.ATRIBUTOSLISTA_CLASSNAMES
            for atributo in atributos_ordenados:
                resultado.append( atributos_objeto[ atributos_clase.index( atributo ) ] )
            # ['categoria', 'cantidad', 'precio_costo', 'minimo', 'precio_venta', 'usa_inventario', 'descripcion', 'codigo']
            usa_inventario = atributos_objeto[ atributos_clase.index( 'usa_inventario' ) ]
            #resultado[2] = int(resultado[2]) if usa_inventario else '-'
            resultado[2] = "%8.2f" % float(resultado[2])
            return resultado

    # REIMPLEMENT TO USE RAM
    def cargarTabla(self,listadeobj = None):       
        if listadeobj == None:
            listadeobj = self.manager.allItems['data']
            #listadeobj = self.manager.getall()
        listadefilas = [self._obtenerValoresAtributos(obj) for obj in listadeobj]
        self.MyTabla.addItems(listadefilas)
        try:
            self.setCantidadItems(len(listadefilas))
        except AttributeError :
            pass

    # REIMPLEMENT TO USE RAM
    def search(self, camponame, valor):
        objs = self.manager.allItems['data']
        attr = self.manager.obtenerNombreAtributo(camponame)
        valor = valor.lower()
        QtGui.QApplication.processEvents()
        results = [
            obj
            for obj in objs
                if obj.__getattribute__(attr)
                    .lower().find(valor) != -1]
        return results

    def makeTableTicket(self):
        columnasTablas = [p.keys()[0] for p in self.ATRIBUTOSLISTA_TICKET]
        self.tablaTicket = MyTableWidget(self.twTicket, columnasTablas, self.ALINEACIONLISTA_TICKET, indexColumn = 2, widthColumn = 600)
        
    def _loadAppShortcuts(self):
        BaseGUI._loadAppShortcuts(self)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL+QtCore.Qt.Key_1), self, self.focoBusqueda)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL+QtCore.Qt.Key_2), self, lambda: self.twDatos.setFocus())
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL+QtCore.Qt.Key_3), self, lambda: self.twTicket.setFocus())
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F12), self, self.on_cmdRegistrarVenta_clicked)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F10), self, self.on_cmdCancelarVenta_clicked)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F2), self, self.on_cmdVarios_clicked)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F6), self, self.on_cmdArtComun_clicked)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F7), self, self.on_cmdEntradas_clicked)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F8), self, self.on_cmdSalidas_clicked)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F4), self, self.on_cmdBorrarArticulo_clicked)
        
    ###
    ### LOGIC ATAJOS METODOS
    ###

    def menuMasAtajos(self):
        menu = QtGui.QMenu(self.cmdMasAtajos)
        #~ proveedor = menu.addAction("Proveedor")
        # database= menu.addAction("Database")
        # busqueda = menu.addAction("Busqueda")
        #~ menu.addSeparator()
        #~ menu.addAction("Mostrar productos favoritos")
        menu.addAction("Ver combinaciones de teclas", self.showCombTeclas)
        menu.addAction("Detalle de ventas", self.showDetalleVentas)
        # menu.addSeparator()
        # menu.addAction("Acerca de..")

        #~ menu_proveedor = QtGui.QMenu()
        #~ menu_proveedor.addAction("Agregar nueva deuda")
        #~ menu_proveedor.addAction("Registrar pago de una deuda")
        #~ proveedor.setMenu(menu_proveedor)
        self.cmdMasAtajos.setMenu(menu)
    
    def showCombTeclas(self):
        from comb_teclas import CombinacionesDeTeclas
        self.ventanita = CombinacionesDeTeclas(self.parent)
        self.ventanita.show()
        
    def showDetalleVentas(self):
        from pos.ventas import Ventas
        self.ventanita = Ventas(
            parent = self.parent,
            manager = self.ventasManager,
            managers = [self.managers[3]]
        )
        self.ventanita.show()
        
    def focoBusqueda(self):
        self.leBusqueda.selectAll()
        self.leBusqueda.setFocus()

    ###
    ### LOGIC VENTA METODOS
    ###

    def getItemsTicket(self):
        # genera una lista de lista con el formato como para cargarce en la tabla
        items = []
        productos = self.ventasManager.productosActuales()
        for producto in productos :
            cantidad = self.ventasManager.obtenerCantidadProducto(producto)
            subtotal = "%8.2f" % (cantidad * producto.precio_venta)
            items.append([
                producto.codigo,
                cantidad,
                producto.descripcion,
                "%8.2f" % producto.precio_venta,
                subtotal
                ])
        return items

    def agregarProductoAVenta(self, producto):
        self.ventasManager.agregarRenglon(producto)
        self.lbTotal.setText("$ %8.2f" % self.ventasManager.obtenerTotal())
        self.tablaTicket.addItems(self.getItemsTicket())
        self.actualizarCantidadProductos()

    def reestablecerCampos(self):
        self.lbTotal.setText('$ 00.00')
        self.tablaTicket.fullClear()
        self.actualizarCantidadProductos()
        self.recargarLista()
        self.leBusqueda.setFocus()

    def actualizarCantidadProductos(self):
        cantidad = self.ventasManager.obtenerCantidadProductos()
        self.lbCantidadProductos.setText("%s productos en la venta actual" % cantidad)

    def cambiarCantidadProducto(self, producto, cantidad):
        self.ventasManager.cambiarCantidadProducto(producto, cantidad)
        self.tablaTicket.addItems(self.getItemsTicket())
        self.actualizarCantidadProductos()
        self.lbTotal.setText("$ %8.2f" % self.ventasManager.obtenerTotal())
        
###############################################################################
###### GUI METHODS
###############################################################################
    
    ###
    ### TABLA BUSQUEDA METODOS
    ###

    def on_twDatos_itemActivated(self , item):
        producto = self.actual_rows_to_objects()
        if producto:
            producto = producto[0]
            if producto.usa_inventario and producto.cantidad == 0:
                QtGui.QMessageBox.warning(self, u" ",u"No posee mas stock en inventario de este producto.")                
            elif self.ventasManager.obtenerCantidadProducto(producto) == producto.cantidad:
                if not producto.usa_inventario:
                    self.agregarProductoAVenta(producto)
                else:
                    QtGui.QMessageBox.warning(self, u" ",u"No queda mas stock de este producto, para poder agregarse a la venta.")
            else:
                self.agregarProductoAVenta(producto)
                
    ###
    ### ATAJOS METODOS
    ###

    @QtCore.pyqtSlot()
    def on_cmdRegistrarVenta_clicked(self):
        if self.ventasManager.obtenerCantidadProductos() > 0 :
            from cobrar import Cobrar
            self.cobrar = Cobrar(self,self.ventasManager)
            self.cobrar.show()
    
    @QtCore.pyqtSlot()
    def on_cmdCancelarVenta_clicked(self):
        if self.ventasManager.obtenerCantidadProductos() > 0 :
            result = QtGui.QMessageBox.warning(self, u"Cancelar venta ",
                        u"¿Esta seguro que desea cancelar?",
                        QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if result == QtGui.QMessageBox.Yes:
                self.ventasManager.cancelarVenta()
                self.reestablecerCampos()

    @QtCore.pyqtSlot()
    def on_cmdVarios_clicked(self):
        if self.twTicket.currentItem():
            index_item = self.twTicket.currentItem().row()
            producto, cantidad = self.ventasManager.obtenerRenglon(index_item)
            if producto:
                from varios import Varios
                self.ventanita = Varios(self, producto, cantidad)
                self.ventanita.show()
    
    @QtCore.pyqtSlot()
    def on_cmdArtComun_clicked(self):
        from articulo_comun import ArticuloComun
        self.ventanita = ArticuloComun(self)
        self.ventanita.show()
    
    @QtCore.pyqtSlot()
    def on_cmdEntradas_clicked(self):
        entradaGUI = self.managers[1]
        entradaGUI.on_btAgregar_clicked()
    
    @QtCore.pyqtSlot()
    def on_cmdSalidas_clicked(self):
        salidaGUI = self.managers[2]
        salidaGUI.on_btAgregar_clicked()
    
    @QtCore.pyqtSlot()
    def on_cmdBorrarArticulo_clicked(self):
        if self.twTicket.currentItem() :
            index_item = self.twTicket.currentItem().row()
            producto = self.ventasManager.obtenerRenglon(index_item)[0]
            if producto:
                result = QtGui.QMessageBox.warning(self, u"Confirmar",
                            u"¿Borrar este producto de la venta?",
                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if result == QtGui.QMessageBox.Yes:
                    self.ventasManager.quitarRenglon(producto)
                    self.lbTotal.setText("$ %8.2f" % self.ventasManager.obtenerTotal())
                    self.tablaTicket.addItems(self.getItemsTicket())
                    self.actualizarCantidadProductos()
    
    @QtCore.pyqtSlot()
    def on_cmdMasAtajos_clicked(self):
        pass
    
    
