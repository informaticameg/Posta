#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plasta.gui import BaseGUI
from os.path import join,abspath,dirname 
from PyQt4 import QtCore, QtGui, uic
import GUI.images_rc, cStringIO
import datetime
from venta import Venta
from GUI.mtw_pos import MyTableWidget

class ResumenGUI( BaseGUI ):

    def __init__(self, parent, manager, managers = []):
        BaseGUI.__init__(self, parent, manager, managers)
        
        self.FILENAME = 'resumen/admin.ui'
        self.ALINEACIONLISTA = ['C','C']
        self.setWindowIcon(QtGui.QIcon(':/newPrefix/logo.png'))
        self._operaciones_de_inicio()
        self.establecerFechaHoyDateEdits()
        self.reflejarDatosResumenDelDia(datetime.date.today())

    def _makeTable(self, table):
        if not self.ATRIBUTOSLISTA :
            columnasTablas = [p.capitalize() for p in self._obtener_atributos_names()]
        else:
            self.ATRIBUTOSLISTA_CLASSNAMES = [ self.manager.obtenerNombreAtributo( p.values()[0] ) for p in self.ATRIBUTOSLISTA]
            columnasTablas = [p.keys()[0] for p in self.ATRIBUTOSLISTA]
        self.MyTabla = MyTableWidget(table, columnasTablas, self.ALINEACIONLISTA)
        
    def _operaciones_de_inicio(self):
        UI_CONTENT = cStringIO.StringIO(self.parent.uis[self.FILENAME])
        uic.loadUi(UI_CONTENT, self)

        self.setWindowTitle("Resumenes - P.O.S.T.A.")
        self._loadAppShortcuts()
        self.fullScreen = False
        
        self._centerOnScreen()

    def ordenarLL(self, lista,nroCampo): 
        """Ordena la lista por el metodo burbuja mejorado.
        Recibe una lista de listas y un numero de campo,
        ordenando por el nro de campo indicado.
        """ 
        intercambios=1 
        pasada=1 
        while pasada<len(lista) and intercambios==1: 
            intercambios=0 
            for i in range(0,len(lista)-pasada): 
                if lista[i][nroCampo] > lista[i+1][nroCampo]: 
                    lista[i], lista[i+1] = lista[i+1], lista[i] 
                    intercambios=1 
            pasada += 1 
        return lista 

    def _generateDateList(self, desde, dias):
        dateList = [ desde + datetime.timedelta(days=x) for x in range(0,dias+1) ]
        dict_ventas = {}
        for d in dateList:
            dict_ventas[d] = 0
        return dict_ventas

    def reflejarDatosResumenDelDia(self, _fecha):
        fecha = datetime.datetime(_fecha.year, _fecha.month, _fecha.day,0,0,0) 
        ventas = self.manager.obtenerMontoVentasTotales(fecha)
        entradas = self.manager.obtenerEntradas(fecha)
        total_entradas = entradas + ventas
        
        autoconsumo = self.manager.obtenerSalidas(fecha, u'producto')
        proveedores = 0
        salidas_dinero = self.manager.obtenerSalidas(fecha, u'dinero')
        total_salidas = salidas_dinero + proveedores

        en_caja = total_entradas - total_salidas

        # entradas        
        self.lbVentasTotales.setText("$ %8.2f" % ventas)
        self.lbEntradasDinero.setText("$ %8.2f" % entradas)
        self.lbTotalEntradas.setText("$ %8.2f" % total_entradas)
        
        # salidas
        self.lbAutoConsumo.setText("$ %8.2f" % autoconsumo)
        self.lbProveedores.setText("$ %8.2f" % proveedores)
        self.lbDinero.setText("$ %8.2f" % salidas_dinero)
        self.lbTotalSalidas.setText("$ %8.2f" % total_salidas)
        # dinero en caja
        self.lbEntradas.setText("$ %8.2f" % total_entradas)
        self.lbSalidas.setText("$ %8.2f" % total_salidas)
        self.lbTotalDineroEnCaja.setText("$ %8.2f" % en_caja)

    def getAtributosListaPorDia(self):
        self.ATRIBUTOSLISTA = [ 
        {u'Día':Venta.fecha},
        {u'Monto vendido':Venta.total}
        ]
        
    def getAtributosListaPorMes(self):
        self.ATRIBUTOSLISTA = [ 
        {u'Mes':Venta.fecha},
        {u'Monto vendido':Venta.total}
        ]

    def getAtributosListaPorAnio(self):
        self.ATRIBUTOSLISTA = [ 
        {u'Mes':Venta.fecha},
        {u'Monto vendido':Venta.total}
        ]
        
    def actualizarTablaDia(self):
        desde = self.deDesde.date().toPyDate()
        hasta = self.deHasta.date().toPyDate()
        if desde != hasta:
            ventas = self.manager.obtenerVentasPorRangoDias(desde, hasta)
            
            dias = (hasta - desde).days
            dict_ventas = self._generateDateList(desde, dias)
            monto_total = 0
            # separar ventas por dia
            for v in ventas:
                dict_ventas[v.fecha.date()] += v.total
                monto_total += v.total
            # generar lista de lista con los resultados
            resultados = []
            for d in dict_ventas.keys():
                resultados.append([d,"$ %8.2f" % dict_ventas[d]])
            self.ordenarLL(resultados,0)
            # formatear fecha
            for row in resultados:
                row[0] = row[0].strftime('%d/%m/%Y')
            # generar tabla
            self.lbTotal.setText("$ %8.2f" % monto_total)
            self.getAtributosListaPorDia()
            self._makeTable(self.twDia)
            self.MyTabla.addItems(resultados)
        
    def actualizarTablaMes(self):
        mes = self.deMesMes.date().toPyDate().month
        anio = self.deMesAnio.date().toPyDate().year
        import calendar
        dias_del_mes = calendar.monthrange(anio,mes)[1]
        ventas = self.manager.obtenerVentasPorMes(mes, anio)
        
        dict_ventas = self._generateDateList(datetime.date(anio,mes,1), dias_del_mes-1)
        monto_total = 0
        # separar ventas por dia
        for v in ventas:
            dict_ventas[v.fecha.date()] += v.total
            monto_total += v.total
        # generar lista de lista con los resultados
        resultados = []
        for d in dict_ventas.keys():
            resultados.append([d,"$ %8.2f" % dict_ventas[d]])
        self.ordenarLL(resultados,0)
        # formatear fecha
        for row in resultados:
            row[0] = row[0].strftime('%d/%m/%Y')
        # generar tabla
        self.lbTotal.setText("$ %8.2f" % monto_total)
        self.getAtributosListaPorMes()
        self._makeTable(self.twMes)
        self.MyTabla.addItems(resultados)

    def actializarTablaAnio(self):
        anio = self.deAnio.date().toPyDate().year
        ventas = self.manager.obtenerVentasPorAnio(anio)
        resultados = [
            ['ENERO',0],['FEBRERO',0],['MARZO',0],['ABRIL',0],
            ['MAYO',0],['JUNIO',0],['JULIO',0],['AGOSTO',0],
            ['SEPTIEMBRE',0],['OCTUBRE',0],['NOVIEMBRE',0],
            ['DICIEMBRE',0]
        ]
        monto_total = 0
        # formatear fecha
        for idx, total in enumerate(ventas):
            resultados[idx][1] = "$ %8.2f" % total
            monto_total += total
        # generar tabla
        self.lbTotal.setText("$ %8.2f" % monto_total)
        self.getAtributosListaPorAnio()
        self._makeTable(self.twAnio)
        self.MyTabla.addItems(resultados)

    def establecerFechaHoyDateEdits(self):
        date_edits = [
        self.dtFecha,
        self.deDesde, 
        self.deHasta,
        self.deMesMes,
        self.deMesAnio,
        self.deAnio
        ]
        [de.setDate(datetime.datetime.today()) for de in date_edits]    
        
    @QtCore.pyqtSlot()
    def on_btDetallesVentas_clicked(self):
        from pos.ventas import Ventas
        self.ventanita = Ventas(
            parent = self.parent, 
            manager = self.managers[0],
            managers = [self.managers[1]]
        )
        self.ventanita.show()

    @QtCore.pyqtSlot()
    def on_btListarPorDia_clicked(self):
        self.actualizarTablaDia()

    @QtCore.pyqtSlot()
    def on_btListarPorMes_clicked(self):
        self.actualizarTablaMes()

    @QtCore.pyqtSlot()
    def on_btListarPorAnio_clicked(self):
        self.actializarTablaAnio() 

    def on_dtFecha_dateChanged(self , date):
        self.reflejarDatosResumenDelDia(date.toPyDate())