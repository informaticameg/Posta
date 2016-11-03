#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui.add_window import BaseAddWindow
from PyQt4 import uic, QtGui,QtCore
from os.path import join,abspath,dirname
from producto import Producto
from categoria import Categoria
import GUI.images_rc

class AddProducto( BaseAddWindow ):

    def __init__(self, parent, unManager, itemaeditar = False, managers = []):
        BaseAddWindow.__init__(self, parent, unManager, itemaeditar, managers)
        self.FILENAME = 'producto/agregar.ui'
        self.loadUi()
        self.setWindowIcon(QtGui.QIcon(':newPrefix/desktop_icon/posta_icon_128.png'))
        self.categorias = []
        self.ITEMLIST = [
             {self.leCodigo:Producto.codigo},
             {self.leDescripcion:Producto.descripcion},
             {self.sbPrecioCostoEntero:Producto.precio_costo},
             {self.sbPrecioVentaEntero:Producto.precio_venta},
             {self.chkUtiliza_inventario:Producto.usa_inventario},
             {self.sbCantidad:Producto.cantidad},
             {self.sbStock_minimo:Producto.minimo},
             {self.cbCategoria:Producto.categoria},
        ]
        self.cargarComboCategorias()
        self.lbCodigoExistente.setVisible(False)

        self._operaciones_de_inicio()

        self.leDescripcion.textEdited.connect(lambda text: self.leDescripcion.setText(text.toUpper()))
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F9), self, self.on_btGuardar_clicked)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F10), self, self.on_btGuardarContinuar_clicked)

        if itemaeditar :
            self.btGuardarContinuar.setVisible(False)
            if itemaeditar.usa_inventario :
                self.chkUtiliza_inventario.setChecked(True)
                self.sbCantidad.setEnabled(True)
                self.sbStock_minimo.setEnabled(True)
            self.btGuardar.setText("F9 Editar")
            # carga parte decimal en los widgets
            pd_pc = str(itemaeditar.precio_costo).split('.')[1]
            pd_pc = int(pd_pc + '0') if int(pd_pc) < 10 else int(pd_pc)
            pd_pv = str(itemaeditar.precio_venta).split('.')[1]
            pd_pv = int(pd_pv + '0') if int(pd_pv) < 10 else int(pd_pv)

            self.sbPrecioCostoDecimal.setValue(pd_pc)
            self.sbPrecioVentaDecimal.setValue(pd_pv)

            if itemaeditar.categoria:
                ordenados = [cat.nombre for cat in self.categorias]
                ordenados.sort()
                idx = ordenados.index(itemaeditar.categoria.nombre)
                self.cbCategoria.setCurrentIndex(idx + 1)

    def cargarComboCategorias(self):
        mc = self.managers[1].manager
        self.categorias = mc.getall()
        ordenados = [cat.nombre for cat in self.categorias]
        ordenados.sort()
        self.cbCategoria.clear()
        self.cbCategoria.addItem(u'- Sin categoría -')
        [self.cbCategoria.addItem(cat) for cat in ordenados]

    def getCodigo(self):
        return unicode(self.leCodigo.text().toUtf8(),'utf-8')

    def mostrarErrorCodigoExistente(self):
        self.lbCodigoExistente.setVisible(True)

    def getPrecioCosto(self):
        entero = self.sbPrecioCostoEntero.value()
        dec  = self.sbPrecioCostoDecimal.value()
        return float('%s.%s' % (entero,dec))

    def getPrecioVenta(self):
        entero = self.sbPrecioVentaEntero.value()
        dec  = self.sbPrecioVentaDecimal.value()
        return float('%s.%s' % (entero,dec))

    def guardar(self, listadedatos):
        '''
        Metodo que automatiza el guardado de los datos.
        @param listadedatos:lista de datos perteneciente al init de la clase que maneja
        '''
        st_categoria = listadedatos[7]
        categoria = None
        if st_categoria != u'- Sin categoría -' :
            res = self.manager.almacen.find(
                Categoria,
                Categoria.nombre == st_categoria)
            if res :
                categoria = res[0]
        listadedatos[7] = categoria
        listadedatos[2] = self.getPrecioCosto()
        listadedatos[3] = self.getPrecioVenta()
        return self.manager.add(*listadedatos)

    def editarPropiedades(self):
        '''
        obtiene los datos de EDITITEM y los de los widgets
        los compara y si son distintos edita el atributo del obj
        '''
        datos = self.obtenerDatosWidgets()
        #########################################################
        ## Obtiene la categoria actual
        widget = self.cbCategoria
        st_categoria = unicode(widget.itemText(widget.currentIndex()).toUtf8(),'utf-8')
        # datos[7] -> categoria
        if datos[7] is not None:
            if st_categoria != datos[7].nombre:
                categoria = None
                if st_categoria != u'- Sin categoría -' :
                    res = self.manager.almacen.find(
                        Categoria,
                        Categoria.nombre == st_categoria)
                    if res :
                        categoria = res[0]
                datos[7] = categoria
        datos[2] = self.getPrecioCosto()
        datos[3] = self.getPrecioVenta()
        #########################################################
        propiedadesvalues = self.obtenerDatosIntancia()
        codigo_old = ''
        for p in propiedadesvalues:
            if 'codigo' == p.keys()[0]:
                codigo_old = p['codigo']
                break
        for i,dato in enumerate(datos):
            nombrepropiedad = propiedadesvalues[i].keys()[0]
            valor = propiedadesvalues[i].values()[0]
            if valor != dato:
                self.EDITITEM.__setattr__(nombrepropiedad,dato)
        self.manager._aiUpdateItem(codigo_old, self.EDITITEM)
        return True

    def on_leCodigo_textEdited(self , text):
        self.lbCodigoExistente.setVisible(False)

    @QtCore.pyqtSlot()
    def on_btGuardar_clicked(self):
        if not self.EDITITEM :
            if not self.manager.existeProducto(self.getCodigo()):
                BaseAddWindow.on_btGuardar_clicked(self)
            else:
                self.mostrarErrorCodigoExistente()
        else:
            BaseAddWindow.on_btGuardar_clicked(self)

    @QtCore.pyqtSlot()
    def on_btGuardarContinuar_clicked(self):
        self.leCodigo.setFocus()
        resultado = False
        if not self.manager.existeProducto(self.getCodigo()):
            if self.validarRestriccionesCampos() :
                datos = self.obtenerDatosWidgets()
                resultado = self.guardar(datos) if not self.EDITITEM else self.editar(datos)
                if self.postSaveMethod :
                    self.postSaveMethod()
            self.leCodigo.clear()
            self.leDescripcion.clear()
            self.sbPrecioCostoEntero.setValue(0)
            self.sbPrecioCostoDecimal.setValue(0)
            self.sbPrecioVentaEntero.setValue(0)
            self.sbPrecioVentaDecimal.setValue(0)
            self.chkUtiliza_inventario.setChecked(False)
            self.sbCantidad.setValue(0)
            self.sbStock_minimo.setValue(0)
            return resultado
        else:
            self.mostrarErrorCodigoExistente()

    @QtCore.pyqtSlot()
    def on_btNuevaCategoria_clicked(self):
        categorias_gui = self.managers[1]
        categorias_gui.on_btAgregar_clicked(self.cargarComboCategorias)

    def on_leDescripcion_textEdited(self,cadena):
        cursor = self.leDescripcion.cursorPosition()
        self.leDescripcion.setText(cadena)
        self.leDescripcion.setCursorPosition(cursor)