#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from GUI.mtw_pos import MyTableWidget
from producto import Producto
from producto.add import AddProducto
from os.path import join,abspath,dirname
from PyQt4 import QtCore, QtGui, uic
import GUI.images_rc
import locale

class InventarioGUI( BaseGUI ):

    def __init__(self, parent, windowparent, manager, managers = []):
        BaseGUI.__init__(self, parent, manager, managers)

        self.FILENAME = 'inventario/admin.ui'
        self.DialogAddClass  = AddProducto

        locale.setlocale( locale.LC_ALL, '' )
        self.setWindowIcon(QtGui.QIcon(':/newPrefix/logo.png'))
        self.ALINEACIONLISTA = ['C','L','L','C','C','C','C','C']
        self.ATRI_COMBO_BUSQUEDA = [
        {u'Descripcion del producto':Producto.descripcion},
        {u'Codigo':Producto.codigo},
        ]
        self.ATRIBUTOSLISTA = [
        {u'Codigo':Producto.codigo},
        {u'Categoria':Producto.categoria},
        {u'Descripcion del producto':Producto.descripcion},
        {u'Precio costo':Producto.precio_costo},
        {u'Precio venta':Producto.precio_venta},
        {u'Existencia':Producto.cantidad},
        {u'Inv. Mínimo':Producto.minimo},
        {u'Usa inventario':Producto.usa_inventario},
        ]
        self.windowparent = windowparent
        self._operaciones_de_inicio()
        self.windowparent.hide()

    def _operaciones_de_inicio(self):
        self.loadUi()

        self.setWindowTitle(self.TITULO)
        self.lbTitulo.setText(self.manager.getClassName())
        self._makeTable()

        self.cargarCombobox()
        self.cargarTabla()
        self._loadAppShortcuts()
        self.fullScreen = False

        self._centerOnScreen()
        self.setWindowState(QtCore.Qt.WindowMaximized)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_B), self, self.leBusqueda.setFocus)
        self.setWindowTitle("Inventario - P.O.S.T.A.")
        self.lbTitulo.setText("Productos en inventario")

        self.cargarComboCategorias()
        self.lbProductosBajosExistencia.setText(
            "%s producto(s) bajo(s) en stock" % self.manager.cantidadProductosBajosEnExistencia())

        menu = QtGui.QMenu(self.clbMas)
        menu.addAction(QtGui.QIcon(':newPrefix/drive-1934.png'), "Importar/Exportar...", self.on_btImportar_clicked)
        menu.addAction(QtGui.QIcon(':newPrefix/computer.png'), "Actualizar precios...", self._actualizarPrecios)
        self.clbMas.setMenu(menu)
        self.twDatos.setColumnWidth(3, 320)

    def close(self):
        BaseGUI.close(self)
        self.windowparent.show()

    def _makeTable(self):
        if not self.ATRIBUTOSLISTA :
            columnasTablas = [p.capitalize() for p in self._obtener_atributos_names()]
        else:
            self.ATRIBUTOSLISTA_CLASSNAMES = [ self.manager.obtenerNombreAtributo( p.values()[0] ) for p in self.ATRIBUTOSLISTA]
            columnasTablas = [p.keys()[0] for p in self.ATRIBUTOSLISTA]
        self.MyTabla = MyTableWidget(self.twDatos, columnasTablas, self.ALINEACIONLISTA, indexColumn = 2)
        self.connect(self.MyTabla.widget, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)

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
            resultado[3] = "$ %8.2f" % float(resultado[3]) # precio costo
            resultado[4] = "$ %8.2f" % float(resultado[4]) # precio venta
            resultado[7] = 'SI' if resultado[7] else 'NO' # usa inventario
            return resultado

    def _filtrarPorCategoria(self, value):
        productos = []
        if value != u'TODAS' and value != u'SIN CATEGORIA':
            categoriasManager = self.managers[1].manager
            unaCategoria = categoriasManager.obtenerPorNombre(value)
            productos = self.manager.obtenerPorCategoria(unaCategoria)
        elif value == u'SIN CATEGORIA':
            productos = self.manager.obtenerSinCategoria()
        else:
            productos = self.manager.allItems['data']
        return productos

    def cargarComboCategorias(self):
        categorias = self.managers[1].manager.getall()
        self.cbCategorias.addItem(u'TODAS')
        self.cbCategorias.addItem(u'SIN CATEGORIA')
        categorias = [categoria.nombre for categoria in categorias]
        categorias.sort()
        [self.cbCategorias.addItem(cat) for cat in categorias]

    def _itemTableSelected(self):
        producto = self.actual_rows_to_objects()
        if producto:
            producto = producto[0]
            self.lbProductoNombre.setText(producto.descripcion)
            self.lbProductoPrecioVenta.setText("$ %8.2f" % float(producto.precio_venta))
            self.lbProductoPrecioCosto.setText("$ %8.2f" % float(producto.precio_costo))
            self.lbProductoExistencia.setText(str(producto.cantidad))

    @QtCore.pyqtSlot()
    def on_btCategorias_clicked(self):
        _productosGUI = self.managers[0]
        _categoriasGUI = _productosGUI.managers[0]
        _categoriasGUI.show()

    @QtCore.pyqtSlot()
    def on_btImportar_clicked(self):
        from importar_exportar import ImportarExportar
        self.ie = ImportarExportar(self)
        self.ie.show()

    @QtCore.pyqtSlot()
    def on_btAgregarInventario_clicked(self):
        item = self.actual_rows_to_objects()
        if item :
            item = item[0]
            from addinventario import AddInventario
            self.ai = AddInventario(self.parent, self.manager, item)
            self.ai.postMethod = self.recargarLista
            self.ai.show()

    def on_btProductosBajosEnStock_toggled(self, value):
        if value:
            productos = self.manager.productosBajosEnStock()
            self.cargarTabla(productos)
        else:
            self.cargarTabla()

    @QtCore.pyqtSlot(int)
    def on_cbCategorias_currentIndexChanged(self , index):
        value = unicode(self.cbCategorias.itemText(index).toUtf8(), 'utf-8')
        self.cargarTabla(self._filtrarPorCategoria(value))

    def on_twDatos_currentItemChanged(self , item_a, item_b):
        self._itemTableSelected()

    def on_twDatos_itemClicked(self , item):
        self._itemTableSelected()

    def _actualizarPrecios(self):
        from actualizar_precios import ActualizarPrecios
        self.ap = ActualizarPrecios(self)
        self.ap.show()