#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import *
from datetime import datetime

class Venta (object):
    
    __storm_table__ = "Venta"

    ide = Int(primary = True)
    fecha = DateTime()    
    total = Float()
    paga_con = Float()
    tipo_venta = Unicode()
    
    def __init__(self,  total, paga_con, tipo_venta):
        self.fecha = datetime.today()
        self.total = total
        self.paga_con = paga_con
        self.tipo_venta = tipo_venta
