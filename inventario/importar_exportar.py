#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import os,sys
from PyQt4 import QtCore, QtGui, uic
import GUI.images_rc #@UnusedImport
from importar.importar_xls import ImportXLS
from categoria import Categoria
from producto import Producto
import tools.pathtools, cStringIO

class ImportarExportar(QtGui.QDialog):
    
    def __init__(self, parent):
        self.parent = parent
        self.FILENAME = 'inventario/impexp.ui'
        QtGui.QDialog.__init__(self)
        UI_CONTENT = cStringIO.StringIO(self.parent.parent.uis[self.FILENAME])
        uic.loadUi(UI_CONTENT, self)
        
        self.__centerOnScreen()
        
        self.manager = parent.manager
        self.almacen = parent.manager.almacen

        self.widgetProgresoImp.setVisible(False)
        self.widgetProgresoExp.setVisible(False)
        self.setWindowIcon(QtGui.QIcon(':newPrefix/drive-1934.png'))
        self.setWindowTitle("Importar/Exportar")
        
    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
        
    ###########################################################################
    ### LOGIC methods
    ###########################################################################  
    
    def abrirArchivo(self):
        """ """
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Seleccione el archivo de productos')

        if filename != '' :
            filename = unicode(filename, 'utf-8')
            return filename
        else:
            return ''

    def exportar(self):
        from datetime import datetime
        day_string = datetime.today().strftime('%d-%m-%Y')
        name_file = 'productos_' + day_string
        filename = QtGui.QFileDialog.getSaveFileName(self,"Exportar", name_file)
        if filename:
            filename = unicode(filename, 'utf-8')
            #if filename.find('.xls') == -1:
            #    filename += '.xls'
            return filename
        return '' 

    def getCategoria(self, nombre):
        nombre = nombre.upper()
        resultado = self.almacen.find(Categoria, Categoria.nombre == nombre)
        objs = [obj for obj in resultado]
        if len(objs) > 0:
            return objs[0]
        else:
            # no existe la categoria, se crea
            return self.almacen.add(Categoria(nombre))

    def parseDataRow(self, row):
        codigo = row[0][:-2] if row[0].find('.0') != -1 else row[0]
        descripcion = row[1].upper()
        precio_costo = 0 if row[2] == '' else float(row[2])
        precio_venta = 0 if row[3] == '' else float(row[3])
        existencia = 0 if row[4] == '' else int(float(row[4]))
        usa_inventario = False if existencia == 0 else True
        inv_minimo = 0 if row[5] == '' else int(float(row[5]))
        categoria = self.getCategoria(row[6]).ide if row[6] != '' else None
        return [codigo,descripcion,precio_costo, precio_venta,usa_inventario,
            existencia,inv_minimo,categoria]

    def codigoYaExiste(self, cod):
        return True if len([obj for obj in self.almacen.find(
                        Producto, Producto.codigo == cod)]) > 0 else False

    def actualizarDatosDeProducto(self, data_prod):
        ''' 
        Se asume que el producto ya existe.
        '''
        unProducto = [obj for obj in self.almacen.find(Producto, Producto.codigo == data_prod[0])]
        if len(unProducto) > 0:
            unProducto = unProducto[0]
            categoria = self.getCategoria(data_prod[7]).ide if data_prod[7] != '' else None
            unProducto.descripcion = data_prod[1]
            unProducto.precio_costo = data_prod[2]
            unProducto.precio_venta = data_prod[3]
            unProducto.usa_inventario = data_prod[4]
            unProducto.cantidad = data_prod[5]
            unProducto.minimo = data_prod[6]
            unProducto.categoria = categoria
            self.almacen.flush()
            self.almacen.commit()

    def importarDatos(self, ruta, actualizar_productos):
        '''
        Toma los datos leidos del .xls y los inserta en el programa.
        '''
        try:
            datos = ImportXLS().getDataInRows(ruta,0)[1:]
            # PROCEDIMIENTO A SEGUIR EN LA IMPORTACION:
            # SI el codigo del producto ya existe, se actualizan los datos con los nuevos
            # SI la categoria del producto no existe, se crea y se asocia al producto
            i = 0
            cant = len(datos)
            self.pbProgreso.setMinimum(1)
            self.pbProgreso.setMaximum(cant)
            for prod in datos:
                #unCodigo, unaDesc, unprecio_costo, unPrecio_venta, UI, unCantidad, unMinimo, unCategoria
                data_prod = self.parseDataRow(prod)
                
                # si esto es True, para cada codigo de prod ya existente en el programa
                # se actualizara con los datos nuevos importados
                if self.codigoYaExiste( data_prod[0] ):
                    if actualizar_productos :
                        self.actualizarDatosDeProducto(data_prod)
                else:
                    unProducto = Producto( *data_prod )
                    self.almacen.add( unProducto )
                    i += 1
                    self.pbProgreso.setValue(i)
            # se persisten los datos
            self.almacen.flush()
            self.almacen.commit()
            print 'Importacion terminada con exito...'
            self.parent.manager._aiGetAll()
            self.parent.manager._aiGenerateIndex()
            self.parent.recargarLista()
            QtGui.QMessageBox.information(self, "Importar",
                    u"Importación terminada con éxito.")
        except Exception, msg:
            print 'Se ha producido un error al intentar importar', msg
            QtGui.QMessageBox.information(self, "Importar",
                    u"Se ha producido un error al intentar importar.")
        self.close()

    def getDataToExport(self):
        allProductos = [obj for obj in self.almacen.find(Producto)]
        attrs = [Producto.codigo, Producto.descripcion, Producto.precio_costo,
            Producto.precio_venta, Producto.cantidad, Producto.minimo, Producto.categoria]
        rows = []
        for producto in allProductos:
            prod = self.manager.getDataObject(producto, attrs)
            row = []
            for index, key in enumerate(['codigo','descripcion','precio_costo',
                'precio_venta','cantidad', 'minimo']):
                value = prod[index][key]
                if type(value) is unicode or type(value) is str:
                    value = value.encode('utf8') 
                row.append(value)

            categoria = prod[6]['categoria'].__str__() \
                if prod[6]['categoria'] is not None else ''
            row.append(categoria.encode('utf8'))
            rows.append(row)
        return rows

    def exportarDatos(self, ruta, format):
        try:
            allProductos = self.getDataToExport()
            cant = len(allProductos)
            if cant == 0 :
                QtGui.QMessageBox.warning(self, "Exportar",
                    "No hay productos cargados para exportar.")
                self.close()
                return False
            self.pbProgresoExp.setMinimum(1)
            self.pbProgresoExp.setMaximum(cant)
            
            titles = ['Codigo','Descripcion','Precio Costo',
                'Precio Venta','Existencia','Inv. Minimo', 'Categoria']
            if format == 'XLS':
                from importar import xlwt
                i = 1
                # init xlwt
                font = xlwt.Font()
                font.bold = True
                style = xlwt.XFStyle()
                style.font = font
                wb = xlwt.Workbook()
                ws = wb.add_sheet('Hoja 1')            

                # generate head
                for idx, title in enumerate(titles):
                    ws.write(0, idx, title, style)
                # generate products
                for producto in allProductos:
                    [ws.write(i, index, value) 
                        for index, value in enumerate(producto)]               
                    i += 1
                    self.pbProgresoExp.setValue(i)
                wb.save(ruta + '.xls')
            if format == 'CSV':
                import csv
                _f = open(ruta + '.csv', 'w')
                _w = csv.writer(_f, delimiter=',')
                _w.writerows([titles] + allProductos)
                _f.close()
                self.pbProgresoExp.setValue(cant)

            QtGui.QMessageBox.information(self, "Exportar",
                        u"Exportación terminada con éxito.")
        
        except Exception, msg:
            print 'Se ha producido un error al intentar exportar', msg
            QtGui.QMessageBox.information(self, "Exportar",
                    u"Se ha producido un error al intentar exportar.")
        self.close()

    ###########################################################################
    ### GUI events methods
    ###########################################################################

    @QtCore.pyqtSlot()
    def on_btPlantillaEjemplo_clicked(self):
        filepath = r'inventario\plantilla.xls'
        import subprocess
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filepath))
        elif os.name == 'nt':
            os.startfile(filepath)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', filepath))

    @QtCore.pyqtSlot()
    def on_btUbicacionExp_clicked(self):
        ruta = self.exportar()
        if len(ruta) > 0:
            self.leUbicacionExp.setText(ruta)        
    
    @QtCore.pyqtSlot()
    def on_btImportar_clicked(self):
        ruta = unicode(self.leUbicacionImportar.text().toUtf8(),'utf-8')
        if len(ruta) > 0:
            self.btSalir.setEnabled(False)
            self.btUbucacionImp.setEnabled(False)
            self.chkActualizar.setEnabled(False)
            self.btImportar.setEnabled(False)
            self.widgetProgresoImp.setVisible(True)
            self.importarDatos(ruta, self.chkActualizar.isChecked())
        else:
            QtGui.QMessageBox.warning(self, "Importar",
                "No se ha seleccionado un archivo de productos.")

    @QtCore.pyqtSlot()
    def on_btExportar_clicked(self):
        ruta = unicode(self.leUbicacionExp.text().toUtf8(),'utf-8')
        format = ''
        if self.rbFormatoXLS.isChecked():
            format = 'XLS'
        if self.rbFormatoCSV.isChecked():
            format = 'CSV'
        if len(ruta) > 0 :
            self.btUbicacionExp.setEnabled(False)
            self.btSalir.setEnabled(False)
            self.btExportar.setEnabled(False)
            self.widgetProgresoExp.setVisible(True)
            self.exportarDatos(ruta, format)
        else:
            QtGui.QMessageBox.warning(self, "Exportar",
                "No se ha seleccionado un nombre para el archivo.")

    @QtCore.pyqtSlot()
    def on_btUbucacionImp_clicked(self):
        ruta = self.abrirArchivo()
        if os.path.splitext(os.path.split(ruta)[1])[1] != '.xls' :
            QtGui.QMessageBox.critical(self, "Importar",
                "El archivo seleccionado no es un archivo MS Excel (.xls).")
        else:
            self.leUbicacionImportar.setText(ruta)
    
def main():
    app = QtGui.QApplication(sys.argv)
    window = ImportarExportar()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
