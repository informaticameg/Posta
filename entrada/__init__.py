#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import *

class Entrada (object):
    ''' Corresponde a una entrada de dinero'''
    
    __storm_table__ = "Entrada"

    ide = Int(primary = True)
    fecha = DateTime()
    monto = Float()
    dinero_inicial = Bool()
    motivo = Unicode()
    
    def __init__(self, monto, motivo, inicial=False):
        from datetime import datetime
        self.fecha = datetime.today()
        self.monto = monto
        self.motivo = motivo
        self.dinero_inicial = inicial
