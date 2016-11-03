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

# import xlwt
import xlrd


class ImportXLS :
        
    def getDataInRows(self, libro, hoja) :
        """ 
            Lee todas las filas del la hoja indicada, devolviendolas
            en una tupla de tuplas.
        """
        import xlrd
        # abre el libro para lectura
        book = xlrd.open_workbook(libro)    
        # se "para" en al hoja indicada
        sh = book.sheet_by_index(hoja)
        todo = [] # 
        # recorre las filas de la hoja
        for rx in range(sh.nrows):
            # recupera la fila en el indice actual
            fila = sh.row(rx)
            actual = []
            for campo in fila:        
                actual.append(unicode(campo.value))
            # agrega a la lista principal, conviertiendo
            # la lista actual a tupla 
            todo.append(tuple(actual))
        # convierte a tupla la lista principal
        todo = tuple(todo)
        
        return todo 
