from plasta.logic.manager import BaseManager
from venta import Venta
from entrada import Entrada
from salida import Salida

class ResumenManager( BaseManager ):
    
    def __init__(self, store, reset, managers ):        
        BaseManager.__init__(self, store, reset)
        self.CLASS = Venta
        self._operaciones_de_inicio()
        
        self.ventasManager = managers[0]
        self.entradasManager = managers[1]
        self.salidasManager = managers[2]
        
    def obtenerEntradas(self, fecha):
        obj_entradas = self.almacen.find(Entrada)
        objs = self.__getByFecha(obj_entradas, fecha)
        return sum([obj.monto for obj in objs])
        
    def obtenerSalidas(self, fecha, tipo):
        obj_salidas = self.almacen.find(Salida)
        obj_salidas = [obj for obj in obj_salidas if obj.tipo == tipo]
        objs = self.__getByFecha(obj_salidas, fecha)
        if tipo == 'dinero':
            return sum([obj.monto for obj in objs])
        elif tipo == 'producto':
            return sum([obj.producto_precio for obj in objs])
                
    def obtenerMontoVentasTotales(self, fecha):
        obj_ventas = self.getall()
        ventas = self.__getByFecha(obj_ventas, fecha)
        return sum([venta.total for venta in ventas])
        
    def obtenerVentasPorRangoDias(self, desde, hasta):
        all_ventas = self.getall()
        return [obj for obj in all_ventas 
            if obj.fecha.date() >= desde and obj.fecha.date() <= hasta]

    def obtenerVentasPorMes(self, mes, anio):
        all_ventas = self.getall()
        return [v for v in all_ventas
            if v.fecha.month == mes and v.fecha.year == anio]
    
    def obtenerVentasPorAnio(self, anio):
        all_ventas = self.getall()
        # cada posicion de la lista sera el mes correspondiente
        meses = [0,0,0,0,0,0,0,0,0,0,0,0]
        for obj in all_ventas: 
            if obj.fecha.date().year == anio:
                meses[obj.fecha.date().month - 1] += obj.total
        return meses

    def __getByFecha(self, objs, fecha):
        return [obj 
            for obj in objs
                if obj.fecha.year == fecha.year and 
                obj.fecha.month == fecha.month and 
                obj.fecha.day == fecha.day]
