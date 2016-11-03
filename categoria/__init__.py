#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storm.locals import *


class Categoria (object):
    
    __storm_table__ = "Categoria"

    ide = Int(primary = True)
    nombre = Unicode(allow_none = False)
    
    def __init__(self,  unNombre):
        self.nombre = unNombre
        
    def __str__(self):
        return self.nombre
