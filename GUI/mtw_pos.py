#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
#       Copyright 2011 Fernandez, Emiliano <emilianohfernandez@gmail.com>
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
from PyQt4 import QtCore, QtGui


class MyTableWidget():

    def __init__(self,TW,listadecolumnas, listadealineaciones = [], indexColumn = 1, widthColumn = 400):
        self.__widget = TW
        quitAction = QtGui.QAction("Quit", self.__widget)
        self.__widget.addAction(quitAction)
        self.__widget.horizontalHeader().setDefaultSectionSize(120)
        #NEXT:que divida los campos en la tabla y que ponga bien los numeros
        self.__widget.horizontalHeader().setResizeMode(0)#maximixa los campos en la tabla
        self.__widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.__widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        
        self.__columns = listadecolumnas
        # 'indexColumn' es un integer que representa la 
        # posicion de la columna que se desea establecer el ancho
        self.__indexColumn = indexColumn
        # 'widthColumn' es el valor del ancho para la columna
        self.__widthColumn = widthColumn
        
        if listadealineaciones :
            alineaciones = {
                'L':QtCore.Qt.AlignLeft,
                'C':QtCore.Qt.AlignCenter,
                'R':QtCore.Qt.AlignRight
            }
            self.__columns_align = [alineaciones[ali] for ali in listadealineaciones]
        else:
            self.__columns_align = [QtCore.Qt.AlignCenter] * len(listadecolumnas)

        self.__widget.setColumnCount(len(self.__columns))
        for i in xrange(self.__widget.columnCount()):  # set horizontal headers
            item = QtGui.QTableWidgetItem(self.__columns[i].capitalize())# the text
            item.setTextAlignment(QtCore.Qt.AlignCenter)# the alignment
            self.__widget.setHorizontalHeaderItem(i, item)
    
    def appendItem(self,listadedatos):
        alineaciones = self.__columns_align
        def aux(x, cell):
            item = QtGui.QTableWidgetItem(unicode(cell))# the text
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable )
            item.setTextAlignment( alineaciones[x] )# the alignment
            widget.setItem(y, x, item)        
        widget = self.__widget
        y = widget.rowCount()
        if listadedatos != None:
            listadedatos = map(lambda valor : '' if valor is None else valor, listadedatos)
            widget.setRowCount(y+1)
            [ aux(x, cell) for x,cell in enumerate(listadedatos)]
            widget.setColumnWidth(self.__indexColumn, self.__widthColumn)

    def addItems(self, DATA):
        """
        DATA debe ser una lista de listas
        """
        alineaciones = self.__columns_align
        def addOneItem(listadedatos, y, indexCol, widthCol):
            def aux(x, cell):
                item = QtGui.QTableWidgetItem(unicode(cell))# the text
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable )
                item.setTextAlignment( alineaciones[x] )# the alignment
                widget.setItem(y, x, item)
                # establece el ancho de la columna
                widget.setColumnWidth(indexCol, widthCol)
            QtGui.QApplication.processEvents()                     
            listadedatos = ['' if dato is None else dato for dato in listadedatos ]
            [ aux(x, cell) for x,cell in enumerate(listadedatos)]
                
        if DATA != None:
            widget = self.__widget
            self.fullClear()
            widget.setRowCount(len(DATA))
            [addOneItem(data, indice, self.__indexColumn, self.__widthColumn) for indice, data in enumerate(DATA)]

    def getRowString(self, item = 'null'):
        """Devuelve una tupla con los datos de el tablewidget en la fila seleccionada
        devuelve los datos en unicode"""
        tablewidget = self.__widget
        tamano = tablewidget.columnCount()
        try:
            if item != 'null':
                x = item
            else:
                x = tablewidget.currentItem().row()  
            datos=[]
            for num in range(tamano):
                qs = tablewidget.item(x,num).text()
                datos.append(unicode(qs.toUtf8(),'utf-8'))
            return tuple(datos)
        except Exception :
            return None
    
    def getListSelectedRows(self):         
        seleccionados = self.__widget.selectionModel().selectedRows()
        rows = [self.getRowString(idx.row()) for idx in  seleccionados]        
        return rows

    def getAllItems(self):
        tamano = self.__widget.rowCount()
        allitemstring = [self.getRowString(y) for y in range(tamano)]
        return allitemstring

    def fullClear(self):        
        self.widget.setRowCount(0)
#        [self.__widget.removeRow(i) for i in range( self.__widget.rowCount() )[::-1]]
        
    def __get_widget(self):
        return self.__widget

    def __set_widget(self, value):
        self.__widget = value 

    widget = property(__get_widget, __set_widget, "widget's docstring")

    
    
        
def main():

    return 0

if __name__ == '__main__':
    main()

